import numpy as np
import pandas as pd
import json
from collections import deque
from datetime import datetime, timedelta
from msal import PublicClientApplication
from pprint import pprint

from ..algorithms.adtributor import Adtributor, RecursiveAdtributor
from ..core.contribution_calculator import calculate_contribution_by_addition, calculate_contribution_by_multiplication, calculate_contribution_by_division
from ..utils import MathOperations, safe_div, get_current_line, get_current_function, get_enum_member
from ..titan.titan_api import TitanApi
from ..config.msn_metrics import MSNMetricTree, MSNMetricTreeNode

class MSNBusinessMetricsAnalyzer:

    def __init__(self, alias_account, titan_token="", metric="", verbose=0):
        """
        alias_account: string, alias account
        metric: string, metric name
        """
        self.alias_account = alias_account
        self.titan_api = TitanApi(alias_account, titan_token)
        self.verbose = verbose
        self.time_mode = "Day"

        # init metric map
        msn_metric_tree = MSNMetricTree()
        self.metric_map = msn_metric_tree.get_metric_tree()

        # init metric config
        ret = self._initial_metric_config(metric)
        if ret:
            raise Exception(f"Error: metric {metric} is not supported.")
        
        self.metric = metric

        # init attribution algorithm map
        self.algorithms = {
            'adtributor': self._run_adtributor,
            'r_adtributor': self._run_r_adtributor
        }
        
        # init dataframes
        self.df_metric_comparison = pd.DataFrame()  # store the detailed metric breakdown
        self.df_dimension_breakdown = pd.DataFrame()  # store the detailed dimension breakdown
        self.df_attribution_result = pd.DataFrame()  # store the detailed attribution result

        # init report dataframes
        self.report_metric_breakdown = pd.DataFrame()  # report by metric breakdown
        self.report_attribution = pd.DataFrame()  # report by adtribution analysis
        print("AutoAnalysis initialized.")        


    # ======================== public methods ========================   
    # run analysis step by step
    def run_analysis(self, treatment_date, control_date, filter_str,
                     time_mode = "Day",
                     step=-1,
                     attribution_dimensions = [], 
                     algorithm_name = "adtributor",
                     use_cache = False,
                     **attribution_args):
        
        # set query parameters
        self.treatment_date = treatment_date
        self.control_date = control_date
        self.time_mode = time_mode

        """step1. get metric breakdown"""
        if step == 1 or step == -1:
            self._run_metric_breakdown(filter_str)  

        """step2. get metric comparison by customized dimension"""
        if step == 2 or step == -1:
            self._run_attribution_analysis(filter_str, 
                                           attribution_dimensions, 
                                           algorithm_name,
                                           use_cache,
                                           **attribution_args)        
        return


    def set_metric(self, metric) -> int:
        ret = 0
        ret = self._initial_metric_config(metric)
        if ret:
            raise Exception(f"Error: metric {metric} is not supported.")
        self.metric = metric
        return ret
    

    def set_customized_metric_tree(self, metric_config_json) -> int:
        # self.metric_map = {metric: [MSNMetricTreeNode()]}
        ret = 0
        replaced_metric_set = set()  # record the replaced metrics
        new_metric_tree = {}
        try:
            metric_tree = json.loads(metric_config_json)
            for m, m_config in metric_tree.items():
                if m in self.metric_map:
                    replaced_metric_set.add(m)
                    print(f"{__class__.__name__} Warning: {m} will be replaced.")
                if not m_config:
                    raise Exception(f"Error: metric config of {m} is empty.")
                # assert that if is_direct_query is True, titan_query is not empty
                if m_config.get("is_direct_query", True) and m_config.get("titan_query", "") == "":
                    raise Exception(f"Error: metric {m} is_direct_query is True, but titan_query is empty.")
                if (not m_config.get("is_direct_query", True)) and len(m_config.get("formula", [])) == 0:
                    raise Exception(f"Error: metric {m} formula is empty.")
                if len(m_config.get("formula", [])) != len(m_config.get("coefficient", [])):
                    raise Exception(f"Error: length of formula and coefficient are not matched. \
                        {len(m_config.get('formula', []))} != {len(m_config.get('coefficient', []))}")
                
                op_type = get_enum_member(MathOperations, m_config.get("op_type"))
                if len(m_config.get("formula", [])) > 0 and op_type is None:
                    raise Exception(f"Error: metric {m} op_type {m_config.get('op_type')} is not supported.")
                # insert into metric_map
                m_node = MSNMetricTreeNode(metric_name=m, 
                            formula=m_config.get("formula", []), 
                            op_type=op_type, 
                            coefficient=m_config.get("coefficient", []), 
                            titan_query=m_config.get("titan_query", ""), 
                            is_direct_query=m_config.get("is_direct_query", True))
                new_metric_tree[m] = [m_node]
        except json.JSONDecodeError as e:
            raise e
        
        # update metric_map
        self.metric_map.update(new_metric_tree)

        if replaced_metric_set:
            print(f"{__class__.__name__} Warning: replaced metrics: {replaced_metric_set}")
        
        # TODO: TEST
        print(f"{__class__.__name__} metric_map:{new_metric_tree}")
        print(f"{__class__.__name__} set_customized_metric_tree success.")
        return ret


    def get_metric_tree(self) -> dict:
        def _parse_MSNMetricTreeNode_to_dict(node:MSNMetricTreeNode) -> dict:
            ret = {}
            ret["metric_name"] = node.metric_name
            ret["formula"] = node.formula
            ret["op_type"] = node.op_type.value if node.op_type else None
            ret["coefficient"] = node.coefficient
            ret["titan_query"] = node.titan_query
            ret["is_direct_query"] = node.is_direct_query
            return ret
        
        ret = {}
        for metric, nodes in self.metric_map.items():
            ret[metric] = list(map(_parse_MSNMetricTreeNode_to_dict, nodes))
        return ret

    # ======================== private methods ========================
    # init metric config
    def _initial_metric_config(self, metric):
        ret = 0
        if metric not in self.metric_map:
            return 1
        metric_breakdown_choices = self.metric_map[metric]
        if len(metric_breakdown_choices) == 0:
            return 1
        # TODO: select the first one by default
        self.metric_config = metric_breakdown_choices[0]

        # start parse tree structure
        metric_set = set([metric])
        used_metric_set = set()
        metric_query_map = {}
        combine_metric_query_map = {}
        # build metric query map
        while metric_set:
            m = metric_set.pop()
            if m in used_metric_set:
                continue
            else:
                used_metric_set.add(m)

            ###### build metric query map ######
            metric_breakdown_choices = self.metric_map.get(m, [])
            if len(metric_breakdown_choices) == 0:
                raise Exception(f"Error: metric {m} is undefined.")
            # TODO: select the first one by default
            metric_config = metric_breakdown_choices[0]
            if self.verbose:
                print(f"metric:{m} has formula:{metric_config.formula}, query:{metric_config.titan_query}")
            
            if metric_config.is_direct_query:
                if metric_config.titan_query == "":
                    raise Exception(f"Error: metric {m}'s query is undefined.")
                else:
                    metric_query_map[m] = metric_config.titan_query
            else:
                combine_query_str = self._build_combined_metric_query(metric_config.formula, metric_config.op_type, metric_config.coefficient)
                if combine_metric_query_map == "":
                    raise Exception(f"Error: metric {m} failed to build query. Please check the configuration.")
                combine_metric_query_map[m] = combine_query_str
            
            # Get next level metrics
            if len(metric_config.formula) == 0:
                continue
            for sub_metric in metric_config.formula:
                if sub_metric in used_metric_set:
                    continue
                metric_set.add(sub_metric)
        
        # END while
        self.metric_query_map = metric_query_map 
        self.combine_metric_query_map = combine_metric_query_map
        self.metric_set = used_metric_set
        if self.verbose:
            print(f"{__class__.__name__}|metric_query_map:{self.metric_query_map}")
            print(f"{__class__.__name__}|combine_metric_query_map:{self.combine_metric_query_map}")
        self.metric_query_str = "\n, ".join([f" {v} AS `{k}`" for k, v in self.metric_query_map.items()])
        if self.combine_metric_query_map:
            self.metric_query_str += " \n, " + "\n, ".join([f" {v} AS `{k}`" for k, v in self.combine_metric_query_map.items()])
        return ret


    def _build_combined_metric_query(self, formula = [], op_type = MathOperations.ADDITION, coefficient = []):
        """
        build combined metric query
        """
        query_str = ""
        if len(formula) != len(coefficient) or len(formula) < 1:
            return query_str
        # if coefficient = 1， then ignore it
        new_formula = [f"{formula[i]}" if coefficient[i] == 1 else f"({formula[i]} * {coefficient[i]})" for i in range(len(formula))]
        if op_type == MathOperations.ADDITION:
            query_str = " + ".join(new_formula)
        elif op_type == MathOperations.MULTIPLICATION:
            query_str = " * ".join(new_formula)
        elif op_type == MathOperations.DIVISION:
            query_str = " / ".join(new_formula)
        return query_str
    

    def _cast_metric_dtype(self, df):  
        print(self.metric_set)
        for col in df.columns:
            if col in self.metric_set:
                df[col] = df[col].astype(float)
            else:
                df[col] = df[col].astype(str)


    def _build_date_query(self):
        date_query = ""
        date_filter = ""
        ret = 0
        if self.time_mode == "Day":
            date_query = f"EventDate = toDate('{self.treatment_date}')"
            date_filter = f"(EventDate = toDate('{self.treatment_date}') OR EventDate = toDate('{self.control_date}'))"
            return ret, date_query, date_filter
        
        elif self.time_mode == "R7":
            start_date_t = datetime.strptime(self.treatment_date, "%Y-%m-%d") - timedelta(days=6)
            start_date_c = datetime.strptime(self.control_date, "%Y-%m-%d") - timedelta(days=6)
            date_filter = f"""((EventDate >= toDate('{start_date_t}') AND EventDate <= toDate('{self.treatment_date}')) 
                            OR (EventDate >= toDate('{start_date_c}') AND EventDate <= toDate('{self.control_date}')))"""
            date_query = f"(EventDate >= toDate('{start_date_t}') AND EventDate <= toDate('{self.treatment_date}'))"
            return ret, date_query, date_filter
        
        elif self.time_mode == "R28":
            start_date_t = datetime.strptime(self.treatment_date, "%Y-%m-%d") - timedelta(days=27)
            start_date_c = datetime.strptime(self.control_date, "%Y-%m-%d") - timedelta(days=27)
            date_filter = f"""((EventDate >= toDate('{start_date_t}') AND EventDate <= toDate('{self.treatment_date}')) 
                            OR (EventDate >= toDate('{start_date_c}') AND EventDate <= toDate('{self.control_date}')))"""
            date_query = f"(EventDate >= toDate('{start_date_t}') AND EventDate <= toDate('{self.treatment_date}'))"
            return ret, date_query, date_filter
        else:
            return 1, date_query, date_filter

    def _get_metric_comparison(self, filter_str):
        """
        get metric comparison from ClickHouse
        treatment_date: string, yyyy-mm-dd
        control_date: string, yyyy-mm-dd
        """
        ret, date_query, date_filter = self._build_date_query()
        if ret:
            raise Exception(f"Error: time mode {self.time_mode} is not supported.")

        # TODO: Change Table and Sample Table
        sql = f"""SELECT IF({date_query}, 'Treatment', 'Control') AS Group
                , {self.metric_query_str}
                FROM MSNAnalytics_Sample
                WHERE {date_filter}
                    AND IsNotExcludedStandard_FY24 = 1
                    AND ({filter_str})
                GROUP BY Group""" 
        print(f"sql:\n{sql}")
        data = self.titan_api.query_clickhouse(sql, "MSNAnalytics_Sample")
        if not data:
            print(f"No data returned. Please check the Titan query or the Titan API:{self.titan_api.endpoint}.")
            return pd.DataFrame()
        return pd.DataFrame(data)
    

    def _get_metric_comparison_by_customized_dimension(self, filter_str, dimension_list):
        """
        get metric comparison from ClickHouse
        treatment_date: string, yyyy-mm-dd
        control_date: string, yyyy-mm-dd
        """
        if len(dimension_list) == 0:
            raise Exception("Error: dimension_list is empty.")
        
        titan_table = "MSNAnalytics_Sample"
        clean_dimension_str = ','.join(list(map(lambda x: x.split("AS ")[-1].strip(), dimension_list)))
        dimensions_str = ",".join(dimension_list)

        ret, date_query, date_filter = self._build_date_query()
        if ret:
            raise Exception(f"Error: time mode {self.time_mode} is not supported.")

        sql = f"""SELECT IF({date_query}, 'Treatment', 'Control') AS Group
                , {dimensions_str}
                , {self.metric_query_str}
                FROM {titan_table}
                WHERE {date_filter}
                    AND IsNotExcludedStandard_FY24 = 1
                    AND ({filter_str})
                GROUP BY Group, {clean_dimension_str}""" 
        print(f"sql:\n{sql}")
        data = self.titan_api.query_clickhouse(sql, titan_table)
        if not data:
            print("No data found.")
            return pd.DataFrame()

        return pd.DataFrame(data)

        
    def _parse_formula(self, m_config) -> str:
        """
        parse formula to string
        e.g. mCFV = mCFV/CPV * CPV/UU * UU
        """
        formula = ""
        if m_config.formula is None or len(m_config.formula) <= 0 or len(m_config.formula) != len(m_config.coefficient):
            return formula
        mc = m_config.coefficient
        if m_config.op_type == MathOperations.ADDITION:    
            formula = " + ".join([f"{mc[i]}*{m_config.formula[i]}" for i in range(len(m_config.formula))])
        elif m_config.op_type == MathOperations.MULTIPLICATION:
            formula = " * ".join([f"({mc[i]}*{m_config.formula[i]})" for i in range(len(m_config.formula))])
        elif m_config.op_type == MathOperations.DIVISION:
            formula = " / ".join([f"({mc[i]}*{m_config.formula[i]})" for i in range(len(m_config.formula))])
        # remove "1*" in formula
        formula = formula.replace("1*", "")
        return formula


    def _parse_contribution(self, m_config, record) -> str:
        """
        cast to json, {factor1: contribution1, factor2: contribution2}
        """
        if m_config.formula is None or len(m_config.formula) <= 0 or len(m_config.formula) != len(m_config.coefficient):
            return ""        
        factors = m_config.formula
        data = {}
        for factor in factors:
            if f"{factor}_Contribution%" not in record.index:
                print(f"Error: {factor}_Contribution% not in record.{record.index}")
            contrib = record[f"{factor}_Contribution%"] if f"{factor}_Contribution%" in record else 0
            data[factor] = f"{contrib:.2%}"
        return json.dumps(data)  


    def _level_traverse_calculate_contribution(self):
        """
        Perform a level-order traversal to calculate the contribution of each metric.
        This method initializes a queue with the root metric and traverses through each level of metrics,
        calculating the contribution of each metric based on its configuration. The results are stored in a report DataFrame.
        
        The method performs the following steps:
        1. Initialize a queue with the root metric.
        2. Traverse through each level of metrics.
        3. For each metric, calculate its contribution based on its configuration.
        4. Store the results in a report DataFrame.
        The report DataFrame contains the following columns:
        - metric: The name of the metric.
        - level: The level of the metric in the traversal.
        - parent: The parent metric.
        - treat: The treatment value of the metric.
        - ctrl: The control value of the metric.
        - delta: The difference between the treatment and control values.
        - delta%: The percentage difference between the treatment and control values.
        - formula: The formula used to calculate the metric.
        - contribution%: The contribution percentage of the metric.
        Returns:
            None
        """
        FUNC_NAME = f"{get_current_function()}|"
        # init queue: [(metric, level, parent_metric)]
        queue = deque([(self.metric, 0, None)])
        used_metrics = set()
        report_columns = ["metric", "level", "parent", "treat", "ctrl", "delta", "delta%", "formula", "contribution%"]
        report = []

        # level traverse
        while queue:
            m, level, parent = queue.popleft()
            if self.verbose:
                print(f"{FUNC_NAME}metric:{m}, level:{level}, parent:{parent}")
            if m in used_metrics:
                continue
            used_metrics.add(m)
            record = pd.Series()

            # init record
            record["metric"] = m
            record["level"] = level
            record["parent"] = parent

            raw_record = self.df_metric_comparison.iloc[0]  # default: only 1 row for each comparison.
            record["treat"] = raw_record[f'{m}_treat']
            record["ctrl"] = raw_record[f'{m}_ctrl']
            record["delta"] = record["treat"] - record["ctrl"]
            record["delta%"] = safe_div(record["delta"], record["ctrl"])
            record["formula"] = ""
            record["contribution%"] = ""
            
            # get next level for m if m has NOT been used.
            m_config_choices = self.metric_map.get(m, [])
            m_config = m_config_choices[0] if len(m_config_choices) > 0 else None
            if m_config is None or len(m_config.formula) <= 0:
                print(f"{FUNC_NAME}Warning: {m} has no m_config or formula.")
                report.append(record)
                continue
            # check if all factors in m_config.formula have been calculated
            elif all([f in used_metrics for f in m_config.formula]):
                print(f"{FUNC_NAME}Warning: {m_config.formula} have been calculated.")
                report.append(record)
                continue
            else:
                record["formula"] = self._parse_formula(m_config)
            
            # do calculation for m
            if m_config.op_type == MathOperations.ADDITION:
                calculate_contribution_by_addition(self.df_metric_comparison, m, m_config.formula, m_config.coefficient)
            elif m_config.op_type == MathOperations.MULTIPLICATION:
                calculate_contribution_by_multiplication(self.df_metric_comparison, m, m_config.formula, m_config.coefficient)
            elif m_config.op_type == MathOperations.DIVISION:
                calculate_contribution_by_division(self.df_metric_comparison, m, m_config.formula, m_config.coefficient)
            else:
                print(f"Error: {m_config.op_type} is not supported.")
            
            raw_record = self.df_metric_comparison.iloc[0]  # default: only 1 row for each comparison.
            # json: {factor1: contribution1, factor2: contribution2}
            record["contribution%"] = self._parse_contribution(m_config, raw_record)
            
            # add record to report
            report.append(record.copy())

            # add sub-metrics to queue
            for sub_metric in m_config.formula:
                queue.append((sub_metric, level+1, m)) 

        self.report_metric_breakdown = pd.DataFrame(report, columns=report_columns)
        if not self.report_metric_breakdown.empty \
            and "parent" in self.report_metric_breakdown.columns \
            and "level" in self.report_metric_breakdown.columns:
            self.report_metric_breakdown.set_index(["level", "parent"], inplace=True)

        return
        

    def _run_metric_breakdown(self, filter_str):
        """
        Get metric comparison by metric breakdown.
        This method retrieves metric comparison data based on a given filter string,
        checks the validity of the data, casts the metric data types, and merges 
        treatment and control groups for further analysis. The metric breakdown 
        function is predefined in the configuration file.
        Parameters:
        filter_str (str): The filter string used to query and retrieve metric comparison data.
        Raises:
        Exception: If the retrieved data is empty or does not contain both 'Treatment' and 'Control' groups.
        Returns:
        None
        """
        # 1-1. get metric comparison
        df = self._get_metric_comparison(filter_str)
        # if df is empty or df didnt contains Treatment or Control, raise exception
        if df.empty or not df["Group"].isin(["Treatment", "Control"]).all():
            raise Exception("No enough data found. Please check the Titan query.")
        self._cast_metric_dtype(df)
        if self.verbose:
            print(f"{__class__.__name__} get data with shape: {df.shape}")

        # 1-2. merge two dataframes
        df["key"] = 1
        df_treat = df[df["Group"] == "Treatment"]
        df_ctrl = df[df["Group"] == "Control"]
        self.df_metric_comparison = pd.merge(df_treat, df_ctrl, on=['key'], suffixes=('_treat', '_ctrl'))

        # 1-3. calculate contribution by factor
        result = self._level_traverse_calculate_contribution()
        print(f"metric tree (node, layer, parent): {result}")
        return

    def _run_attribution_analysis(self, filter_str: str, 
                                  attribution_dimensions: list, 
                                  algorithm_name: str, 
                                  use_cache: bool = False,
                                  **kwargs):
        """
        Run attribution analysis on the given data.
        Parameters:
            filter_str (str): The filter string to apply to the data.
            attribution_dimensions (list): List of dimensions to use for attribution analysis.
            algorithm_name (str): The name of the algorithm to use for attribution analysis.
            **kwargs: Additional keyword arguments to pass to the algorithm function.
        Raises:
            Exception: If the algorithm_name is not supported.
            Exception: If attribution_dimensions is empty.
            Exception: If the data frame is empty or does not contain 'Treatment' or 'Control' groups.
        Returns:
            None, self.report_attribution will be updated.
        """
        if algorithm_name not in self.algorithms:
            raise Exception(f"Algorithm {algorithm_name} is not supported. Now only support {list(self.algorithms.keys())}")

        if len(attribution_dimensions) == 0:
            raise Exception("Error: attribution_dimensions is at least one dimension.")

        if use_cache and not self.df_dimension_breakdown.empty:
            # 1. get dimension breakdown data from cache
            df = self.df_dimension_breakdown.copy()    
            attribution_dimensions = list(map(lambda x: x.split("AS ")[-1].strip(), attribution_dimensions))
            # 2. Call the adtributor_analysis, and self.df_attribution_result will be updated here.
            algorithm_func = self.algorithms[algorithm_name]
            algorithm_func(df, attribution_dimensions, "Treatment", "Control", **kwargs)

            # 3. report by adtribution result
            self.report_attribution = self.df_attribution_result    
            return
            
        elif use_cache and self.df_dimension_breakdown.empty:
            print(f"{__class__.__name__} Warning: self.df_metric_comparison is empty. Will run query from Titan first.")
        else:
            pass

        # 1. get metric comparison by customized dimension
        df = self._get_metric_comparison_by_customized_dimension(filter_str, attribution_dimensions)
        # if df is empty or df didnt contains Treatment or Control, raise exception
        if df.empty or not df["Group"].isin(["Treatment", "Control"]).all():
            raise Exception("No data found. Please check the Titan query.")
        
        self._cast_metric_dtype(df)
        if self.verbose:
            print(f"{__class__.__name__} get data by dimension: {df.shape}")

        attribution_dimensions = list(map(lambda x: x.split("AS ")[-1].strip(), attribution_dimensions))
        # refactor the dataframe
        df_t = df[df["Group"] == "Treatment"]
        df_c = df[df["Group"] == "Control"]
        df = pd.merge(df_c, df_t, on = attribution_dimensions, how="outer", suffixes=["_c", "_t"]).fillna(0)
        df.rename(columns={f"{self.metric}_c": "Control", f"{self.metric}_t": "Treatment"}, inplace=True)

        if self.verbose:
            print(f"{__class__.__name__} Input data for adtribution analysis:")
            pprint(df.head())
        
        # if the metric type is ratio, need to calculate the weighted value.
        if self.metric_config.op_type == MathOperations.DIVISION:
            if len(self.metric_config.formula) != 2:
                raise Exception(f"Error: the formula of {self.metric} is not correct.")
            if f"{self.metric_config.formula[1]}_c" not in df.columns \
                or f"{self.metric_config.formula[1]}_t" not in df.columns:
                raise Exception(f"Error: {self.metric_config.formula[1]}_c or {self.metric_config.formula[1]}_t not found in the dataframe.")
            df["Control_weight"] = df[self.metric_config.formula[1] + "_c"] / df[self.metric_config.formula[1] + "_c"].sum()
            df["Treatment_weight"] = df[self.metric_config.formula[1] + "_t"] / df[self.metric_config.formula[1] + "_t"].sum()
            df["Control"] = df["Control"] * df["Control_weight"]
            df["Treatment"] = df["Treatment"] * df["Treatment_weight"]

        self.df_dimension_breakdown = df

        # 2. Call the adtributor_analysis, and self.df_attribution_result will be updated here.
        algorithm_func = self.algorithms[algorithm_name]
        algorithm_func(df, attribution_dimensions, "Treatment", "Control", **kwargs)

        # 3. report by adtribution result
        self.report_attribution = self.df_attribution_result

    
    def _run_adtributor(self, df: pd.DataFrame,
                        dimension_cols: list,
                        treatment_col: str,
                        control_col: str,
                        top_n_factors = 10,
                        TEEP = 0.05,
                        TEP = 1,
                        min_surprise = 0.0005,
                        max_item_num = 10,
                        need_negative_ep_factor = False,
                        verbose = 0):
        """
        TEEP: Minimum detectable EP value
        TEP: EP cumulative threshold
        dimension_cols must be found in data
        treatment_col and control_col must be found in data
        """
        # check if the columns are in the dataframe
        if not set(dimension_cols + [treatment_col, control_col]).issubset(set(df.columns)):
            raise Exception(f"Columns:{dimension_cols + [treatment_col, control_col]} not found in the dataframe.")
                
        analyzer = Adtributor(top_n_factors = top_n_factors,
                        TEEP = TEEP, 
                        TEP = TEP,
                        min_surprise = min_surprise, 
                        max_item_num = max_item_num,
                        need_negative_ep_factor = need_negative_ep_factor,
                        verbose = verbose)

        self.df_attribution_result = analyzer.analyze(
            data = df, 
            dimension_cols = dimension_cols, 
            treatment_col = treatment_col, 
            control_col = control_col)
        
        return

    def _run_r_adtributor(self, df: pd.DataFrame,
                        dimension_cols: list,
                        treatment_col: str,
                        control_col: str,
                        top_n_factors = 10,
                        TEEP = 0.05,
                        TEP = 1,
                        min_surprise = 0.0005,
                        max_item_num = 3,
                        max_dimension_num = 3,
                        max_depth = 3,
                        need_negative_ep_factor = False,
                        need_prune = True,
                        verbose = 0):
        """
        TEEP: Minimum detectable EP value
        TEP: EP cumulative threshold
        dimension_cols must be found in data
        treatment_col and control_col must be found in data
        """
        # check if the columns are in the dataframe
        if not set(dimension_cols + [treatment_col, control_col]).issubset(set(df.columns)):
            raise Exception(f"Columns:{dimension_cols + [treatment_col, control_col]} not found in the dataframe.")

        analyzer = RecursiveAdtributor(top_n_factors = top_n_factors,
                        TEEP = TEEP, 
                        TEP = TEP,
                        min_surprise = min_surprise, 
                        max_item_num = max_item_num,
                        max_dimension_num = max_dimension_num,
                        max_depth = max_depth,
                        need_negative_ep_factor = need_negative_ep_factor,
                        need_prune = need_prune,
                        verbose = verbose)

        self.df_attribution_result = analyzer.analyze(
            data = df, 
            dimension_cols = dimension_cols, 
            treatment_col = treatment_col, 
            control_col = control_col)
        
        return        
    