from ..utils import *

"""
This module provides functions to calculate the contribution of various factors to a given metric using different methods: addition, multiplication, and division.
Functions:
    calculate_contribution_by_addition(df, metric, factors=[], coefficient=[]):
        Calculates the contribution of each factor to the metric by addition.
        Args:
            df (pd.DataFrame): DataFrame containing the data.
            metric (str): The metric to calculate contributions for.
            factors (list): List of factors to calculate contributions for.
            coefficient (list): List of coefficients for each factor.
    calculate_contribution_by_multiplication(df, metric, factors=[], coefficient=[]):
        Calculates the contribution of each factor to the metric by multiplication using logarithms.
        Args:
            df (pd.DataFrame): DataFrame containing the data.
            metric (str): The metric to calculate contributions for.
            factors (list): List of factors to calculate contributions for.
            coefficient (list): List of coefficients for each factor.
    calculate_contribution_by_division(df, metric, factors=[], coefficient=[]):
        Calculates the contribution of each factor to the metric by division using logarithms.
        Args:
            df (pd.DataFrame): DataFrame containing the data.
            metric (str): The metric to calculate contributions for.
            factors (list): List of factors to calculate contributions for. Must contain exactly 2 factors.
            coefficient (list): List of coefficients for each factor.

"""

def calculate_contribution_by_addition(df, metric, factors=[], coefficient=[]):
        # total metric delta
        if f'delta_{metric}' not in df.columns or f'delta%_{metric}' not in df.columns:
            df[f'delta_{metric}'] = df[f'{metric}_treat'] - df[f'{metric}_ctrl']
            df[f'delta%_{metric}'] = df.apply(lambda x: safe_div(x[f'delta_{metric}'], x[f'{metric}_ctrl']), axis=1)

        # calculate each factor's contribution
        for i, factor in enumerate(factors):
            df[f'delta_{factor}'] = df[f'{factor}_treat'] - df[f'{factor}_ctrl']
            df[f'delta%_{factor}'] = df.apply(lambda x: safe_div(x[f'delta_{factor}'], x[f'{factor}_ctrl']), axis=1)
            df[f'{factor}_Contribution%'] = df[f'delta_{factor}']*coefficient[i] / df[f'delta_{metric}']
        

def calculate_contribution_by_multiplication(df, metric, factors=[], coefficient=[]):
    # total metric delta
    if f'delta_{metric}' not in df.columns or f'delta%_{metric}' not in df.columns:
        df[f'delta_{metric}'] = df[f'{metric}_treat'] - df[f'{metric}_ctrl']
        df[f'delta%_{metric}'] = df.apply(lambda x: safe_div(x[f'delta_{metric}'], x[f'{metric}_ctrl']), axis=1)
    
    # using log to calculate each factor's contribution
    df[f'delta_{metric}_log'] = np.log(df[f'{metric}_treat']) - np.log(df[f'{metric}_ctrl'])
    for i, factor in enumerate(factors):
        df[f'delta_{factor}_log'] = np.log(df[f'{factor}_treat'] * coefficient[i]) - np.log(df[f'{factor}_ctrl'] * coefficient[i])
        # df[f'delta%_{factor}'] = df.apply(lambda x: safe_div(x[f'delta_{factor}'], x[f'{factor}_ctrl']), axis=1)
        df[f'{factor}_Contribution%'] = df[f'delta_{factor}_log'] / df[f'delta_{metric}_log']
    

def calculate_contribution_by_division(df, metric, factors=[], coefficient=[]):
    # suggest the length of division's factor is 2
    if len(factors) != 2:
        print(f"Error: division's factor must be 2.")
        return
    if f'delta_{metric}' not in df.columns or f'delta%_{metric}' not in df.columns:
        df[f'delta_{metric}'] = df[f'{metric}_treat'] - df[f'{metric}_ctrl']
        df[f'delta%_{metric}'] = df.apply(lambda x: safe_div(x[f'delta_{metric}'], x[f'{metric}_ctrl']), axis=1)

    # calculate each factor's contribution.
    df[f'delta_{metric}_log'] = np.log(df[f'{metric}_treat']) - np.log(df[f'{metric}_ctrl'])
    # numerator
    df[f'delta_{factors[0]}'] = df[f'{factors[0]}_treat'] - df[f'{factors[0]}_ctrl']
    df[f'delta%_{factors[0]}'] = df.apply(lambda x: safe_div(x[f'delta_{factors[0]}'], x[f'{factors[0]}_ctrl']), axis=1)
    df[f'{factors[0]}_Contribution%'] = (np.log(df[f'{factors[0]}_treat'] * coefficient[0]) - np.log(df[f'{factors[0]}_ctrl'] * coefficient[0])) / df[f'delta_{metric}_log']
    # denominator
    df[f'delta_{factors[1]}'] = df[f'{factors[1]}_treat'] - df[f'{factors[1]}_ctrl']
    df[f'delta%_{factors[1]}'] = df.apply(lambda x: safe_div(x[f'delta_{factors[1]}'], x[f'{factors[1]}_ctrl']), axis=1)
    df[f'{factors[1]}_Contribution%'] = -(np.log(df[f'{factors[1]}_treat'] * coefficient[1]) - np.log(df[f'{factors[1]}_ctrl'] * coefficient[1])) / df[f'delta_{metric}_log']