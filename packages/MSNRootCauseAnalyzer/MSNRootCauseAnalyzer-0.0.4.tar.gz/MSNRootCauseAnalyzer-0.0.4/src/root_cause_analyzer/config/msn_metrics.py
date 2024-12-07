
from .base_metric_config import BaseMetricConfig, BaseMetricNode
from ..utils import MathOperations


class MSNMetricTree:
    def __init__(self):
        """
        When adding new metric, need to add the metric to the metric_tree
        Once MSNMetricTree is initialized, the metric_tree will be created.
        TODO: If it's a service code, it should be initialized in the service starting stage, and read all metrics from db.
        TODO: to support multiple metric break down choices.
        """
        self.metric_tree = {
            "mCFV": [
                        MSNMetricTreeNode(metric_name="mCFV", 
                                  formula=["mCFV/CPV", "CPV/UU", "UU"],
                                  op_type=MathOperations.MULTIPLICATION, 
                                  coefficient=[1, 1, 1], 
                                  titan_query="SUM(mCFV_FY24)", 
                                  is_direct_query=True),
                    ],
            "mCFV/CPV": [
                    MSNMetricTreeNode(metric_name="mCFV/CPV",
                                    formula=[],
                                    op_type=None,
                                    coefficient=[],
                                    titan_query="SUM(mCFV_FY24) / SUM(IF(UserAction = 'View', IsCorePV, 0))",
                                    is_direct_query=True),
                    ], 
            "CPV": [
                        MSNMetricTreeNode(metric_name="CPV",
                                    formula=["CPV/UU", "UU"],
                                    op_type=MathOperations.MULTIPLICATION,
                                    coefficient=[1, 1],
                                    titan_query="SUM(IF(UserAction = 'View', IsCorePV, 0))",
                                    is_direct_query=True),
                    ],
            "CSDAU": [
                    MSNMetricTreeNode(metric_name="CSDAU",
                                    formula=["Visitor", "CSDAU/Visitor"],
                                    op_type=MathOperations.MULTIPLICATION,
                                    coefficient=[1, 1],
                                    titan_query="SUM(IsCSDAU_FY25)",
                                    is_direct_query=True)
                    ],
            "Visitor": [
                MSNMetricTreeNode(metric_name="Visitor",
                                    formula=[],
                                    op_type=None,
                                    coefficient=[],
                                    titan_query="SUM(IF(IsMUIDStable = 1 OR Canvas in ('Distribution'), 1, 0))",
                                    is_direct_query=True)
                ],
            "CSDAU/Visitor": [
                    MSNMetricTreeNode(metric_name="CSDAU/Visitor",
                                    formula=["CSDAU", "Visitor"],
                                    op_type=MathOperations.DIVISION,
                                    coefficient=[1, 1],
                                    titan_query="",
                                    is_direct_query=False)
                    ],
            "FVR": [
                MSNMetricTreeNode(metric_name="FVR",
                                formula=["FullLayoutCPVRate", "PeekLayoutCPVRate", "ContentOffCPVRate"],
                                op_type=MathOperations.ADDITION,
                                coefficient=[1, 0.33, 0],
                                titan_query="SUM(multiIf((UserAction = 'View' AND IsCorePV = 1 AND (PageContentLayout in ('Informational', 'Custom - Content visible') OR Canvas like '%App%')), 1, " \
                                + " (UserAction = 'View' AND IsCorePV = 1 AND PageContentLayout in ('Inspirational Peek', 'Custom - Content Feed Peek', 'Inspirational')), 0.33, 0)) "\
                                + " / SUM(IF(UserAction = 'View', IsCorePV, 0))",
                                is_direct_query=True)    
                ],
            "FullLayoutCPVRate": [
                                MSNMetricTreeNode(metric_name="FullLayoutCPVRate",
                                formula=["FullLayoutCPV", "CPV"],
                                op_type=MathOperations.DIVISION,
                                coefficient=[1, 1],
                                titan_query="",
                                is_direct_query=False)
                ],
            "PeekLayoutCPVRate": [
                            MSNMetricTreeNode(metric_name="PeekLayoutCPVRate",
                            formula=["PeekLayoutCPV", "CPV"],
                            op_type=MathOperations.DIVISION,
                            coefficient=[1, 1],
                            titan_query="",
                            is_direct_query=False)
                ],

            "ContentOffCPVRate": [
                            MSNMetricTreeNode(metric_name="ContentOffCPVRate",
                            formula=["ContentOffCPV", "CPV"],
                            op_type=MathOperations.DIVISION,
                            coefficient=[1, 1],
                            titan_query="",
                            is_direct_query=False)],
                      
            "FullLayoutCPV": [
                            MSNMetricTreeNode(metric_name="FullLayoutCPV",
                            formula=["FullLayoutCPVPerUU", "FullLayoutUU"],
                            op_type=MathOperations.MULTIPLICATION,
                            coefficient=[1, 1],
                            titan_query="SUM(IF(UserAction = 'View' AND IsCorePV = 1 AND (PageContentLayout in ('Informational', 'Custom - Content visible') OR Canvas like '%App%'), 1, 0))",
                            is_direct_query=True), 
                ],
            "PeekLayoutCPV": [
                            MSNMetricTreeNode(metric_name="PeekLayoutCPV",
                            formula=["PeekLayoutCPVPerUU", "PeekLayoutUU"],
                            op_type=MathOperations.MULTIPLICATION,
                            coefficient=[1, 1],
                            titan_query="SUM(IF(UserAction = 'View' AND IsCorePV = 1 AND PageContentLayout in ('Inspirational Peek', 'Custom - Content Feed Peek', 'Inspirational'), 1, 0))",
                            is_direct_query=True)
            ],
            "ContentOffCPV": [
                            MSNMetricTreeNode(metric_name="ContentOffCPV",
                            formula=["ContentOffCPVPerUU", "ContentOffUU"],
                            op_type=MathOperations.MULTIPLICATION,
                            coefficient=[1, 1],
                            titan_query="SUM(IF(UserAction = 'View' AND PageContentLayout in ('Custom - Content off', 'Custom - Headings Only', 'Focus', 'Custom - Content visible on scroll'), IsCorePV, 0))",
                            is_direct_query=True)
            ],

            "FullLayoutCPVPerUU": [
                            MSNMetricTreeNode(metric_name="FullLayoutCPVPerUU",
                            formula=["FullLayoutCPV", "FullLayoutUU"],
                            op_type=MathOperations.DIVISION,
                            coefficient=[1, 1],
                            titan_query="",
                            is_direct_query=False)
            ],

            "PeekLayoutCPVPerUU": [
                            MSNMetricTreeNode(metric_name="PeekLayoutCPVPerUU",
                            formula=["PeekLayoutCPV", "PeekLayoutUU"],
                            op_type=MathOperations.DIVISION,
                            coefficient=[1, 1],
                            titan_query="",
                            is_direct_query=False)
            ],

            "ContentOffCPVPerUU": [
                            MSNMetricTreeNode(metric_name="ContentOffCPVPerUU",
                            formula=["ContentOffCPV", "ContentOffUU"],
                            op_type=MathOperations.DIVISION,
                            coefficient=[1, 1],
                            titan_query="",
                            is_direct_query=False)
            ],

            "FullLayoutUU": [
                            MSNMetricTreeNode(metric_name="FullLayoutUU",
                            formula=["FullLayoutUserShare", "UU"],
                            op_type=MathOperations.MULTIPLICATION,
                            coefficient=[1, 1],
                            titan_query="COUNT(DISTINCT IF(PageContentLayout in ('Informational', 'Custom - Content visible'), UserMUIDHash, NULL))",
                            is_direct_query=True)
            ],
            "PeekLayoutUU": [
                            MSNMetricTreeNode(metric_name="PeekLayoutUU",
                            formula=["PeekLayoutUserShare", "UU"],
                            op_type=MathOperations.MULTIPLICATION,
                            coefficient=[1, 1],
                            titan_query="COUNT(DISTINCT IF(PageContentLayout in ('Inspirational Peek', 'Custom - Content Feed Peek'), UserMUIDHash, NULL))",
                            is_direct_query=True)],

            "ContentOffUU": [
                            MSNMetricTreeNode(metric_name="ContentOffUU",
                            formula=["ContentOffUserShare", "UU"],
                            op_type=MathOperations.MULTIPLICATION,
                            coefficient=[1, 1],
                            titan_query="COUNT(DISTINCT IF(PageContentLayout in ('Custom - Content off', 'Custom - Headings Only', 'Focus', 'Custom - Content visible on scroll'), UserMUIDHash, NULL))",
                            is_direct_query=True)
            ],

            "FullLayoutUserShare": [
                            MSNMetricTreeNode(metric_name="FullLayoutUserShare",
                            formula=["FullLayoutUU", "UU"],
                            op_type=MathOperations.DIVISION,
                            coefficient=[1, 1],
                            titan_query="",
                            is_direct_query=False)
            ],

            "PeekLayoutUserShare": [
                            MSNMetricTreeNode(metric_name="PeekLayoutUserShare",
                            formula=["PeekLayoutUU", "UU"],
                            op_type=MathOperations.DIVISION,
                            coefficient=[1, 1],
                            titan_query="",
                            is_direct_query=False)
            ],

            "ContentOffUserShare": [
                            MSNMetricTreeNode(metric_name="ContentOffUserShare",
                            formula=["ContentOffUU", "UU"],
                            op_type=MathOperations.DIVISION,
                            coefficient=[1, 1],
                            titan_query="",
                            is_direct_query=False)
            ],

            "CPV/UU": [
                        MSNMetricTreeNode(metric_name="CPV/UU",
                                formula=["CPV", "UU"],
                                op_type=MathOperations.DIVISION,
                                coefficient=[1, 1],
                                titan_query="",
                                is_direct_query=False)
                    ],
            "UU": [
                    MSNMetricTreeNode(metric_name="UU",
                                formula=[],
                                op_type=None,
                                coefficient=[],
                                titan_query="COUNT(DISTINCT UserMUIDHash)",
                                is_direct_query=True)
            ]

        }      

    def get_metric_tree(self):
        return self.metric_tree
    

class MSNMetricTreeNode(BaseMetricNode):
    def __init__(self, metric_name, formula, op_type, coefficient, titan_query, is_direct_query=True):
        """
        metric_name: str
        formula: list, the formula of the metric, e.g. ["CPV/UU", "UU"]
        op_type: MathOperations, the operation type of the metric, e.g. MathOperations.MULTIPLICATION
        coefficient: list, the coefficient of the formula, e.g. [1, 1]
        titan_query: str, the query string for titan
        is_direct_query: bool, whether the metric is a direct query or not. If it's not a direct query, the metric will be calculated based on the formula.
        """
        super().__init__()
        if len(formula) != len(coefficient):
            raise ValueError(f"{metric_name}: The length of formula and coefficient should be the same. len(formula): {len(formula)} != len(coefficient): {len(coefficient)}")
        self.metric_name = metric_name
        self.formula = formula
        self.op_type = op_type
        self.coefficient = coefficient
        self.titan_query = titan_query
        self.is_direct_query = is_direct_query


Titan_Query_Dimension_Template = {
            "Canvas": """CASE WHEN Canvas IN ('Anaheim DHP', 'Anaheim NTP', 'EnterpriseNews NTP') THEN 'All-Up Anaheim'
            WHEN Canvas IN ('WindowsShell Taskbar', 'WindowsP2Shell', 'Enterprise WindowsP2Shell') THEN 'Prong1&2'
            WHEN Canvas IN ('Win 10 Prime', 'Downlevel Prime') THEN 'msn.com'
            WHEN Canvas IN ('AndroidApp', 'IOSApp') THEN 'SuperApp'
            ELSE 'Others' END AS Canvas_""",  # add suffix to avoid conflict with other columns
            
            "Browser": """CASE WHEN lower(Browser) LIKE '%edg%' THEN 'Edge'
            ELSE 'Others' END AS Browser_""",
            
            "PageType": """CASE WHEN lower(PageVertical) == 'homepage' THEN 'Homepage' 
            WHEN lower(PageType) IN ('article', 'gallery', 'video', 'watch') THEN 'Consumption'
            WHEN lower(PageType) NOT IN ('article', 'gallery', 'video', 'watch') 
            AND lower(PageVertical) IN ('sports', 'weather', 'traffic', 'finance', 'casualgames', 'shopping', 'autos') 
            THEN 'Verticals'
            ELSE 'Others' END AS PageType_""",

            "Product": """CASE WHEN Product IN ('anaheim', 'entnews') THEN Product
            WHEN Product IN ('windowsshell', 'windowsdash', 'entwindowsdash', 'windows') THEN Product
            WHEN Product IN ('SuperAppHP', 'SuperAppNews', 'SuperAppBing') THEN Product
            ELSE 'Others' END AS Product_"""
        }

Titan_Query_Dimension_Value_Template = {
    "Canvas": {
        "All-Up Anaheim": "Canvas IN ('Anaheim DHP', 'Anaheim NTP', 'EnterpriseNews NTP')",
        "Prong1&2": "Canvas IN ('WindowsShell Taskbar', 'WindowsP2Shell', 'Enterprise WindowsP2Shell')",
        "msn.com": "Canvas IN ('Win 10 Prime', 'Downlevel Prime')",
        "SuperApp": "Canvas IN ('AndroidApp', 'IOSApp')"
    },
    "Browser": {
        "Edge": "lower(Browser) LIKE '%edg%'"
    },
    "PageType": {
        "Homepage": "lower(PageVertical) == 'homepage'",
        "Consumption": "lower(PageType) IN ('article', 'gallery', 'video', 'watch')",
        "Verticals": """lower(PageType) NOT IN ('article', 'gallery', 'video', 'watch') 
                        AND lower(PageVertical) IN ('sports', 'weather', 'traffic', 'finance', 'casualgames', 'shopping', 'autos')"""
    },
    "Product": {
    }
}