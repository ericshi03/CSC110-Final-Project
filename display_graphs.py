"""
Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Danesh Kohina, Enfei Zhang, Eric Shi, Jefferson Liu

This file will take in data and use the plotly, statsmodel, and pandas modules to
graphically represent the correlation between our calculated risk factor and a factor
of our choosing.
"""
from typing import Optional
from pandas import DataFrame
import plotly.express as px
import classes


def convert_to_dataframe(values: list[classes.Industry]) -> DataFrame:
    """
    This function will convert the list of Industries into a dataframe class to ensure
    ease of use when working with plotly.
    """
    names = []
    lay_off_per_avg = []
    revenue_avg = []
    expenses_avg = []
    vuln_val = []
    # for loop will go through the list of Industry classes to extract relevant data
    for val in values:
        names.append(val.name)
        lay_off_per_avg.append(sum(val.layoffPercentages) / len(val.layoffPercentages))
        revenue_avg.append(val.revenue[0])
        expenses_avg.append(val.expenses[0])
        vuln_val.append(val.vulnerability)
    # Extra line for improved clarity
    processed_values = {'Industries': names, 'Lay Off Percentages': lay_off_per_avg,
                        'Revenue': revenue_avg, 'Expenses': expenses_avg,
                        'Vulnerability Values': vuln_val}
    return DataFrame(data=processed_values)


def display_linear_graphs(df: DataFrame, factor: Optional[str] = 'Expenses') -> None:
    """
    This function will take in a DataFrame class and will output a graph based on the factor
    specified. This function will also perform a Linear Regression on the graph to determine
    a value of R^2.

    Preconditions:
        - factor in ['Revenue', 'Expenses', 'Lay Off Percentages']
        - 'Revenue' in b and 'Expenses' in b and 'Lay Off Percentages' in b
    """
    # Creates the figure object
    fig = px.scatter(df, x=factor, y='Vulnerability Values', color='Industries',
                     trendline='ols', trendline_scope='overall',
                     title="The Effect of " + factor + " compared to Vulnerability Values")

    # Calculates the trendline and Linear Regression
    results = px.get_trendline_results(fig)
    results = results.iloc[0]["px_fit_results"].summary()

    rfinder = [str(results).split()[x] for x in range(len(str(results).split()))
               if str(results).split()[x - 1] == 'R-squared:']

    # Displays the R^2 on the graph, can be reworked to include more text if needed
    shift = -4
    if factor != 'Lay Off Percentages:':
        shift = 0

    fig.add_annotation(x=shift, text='R<sup>2</sup> = '
                                     + str(rfinder[0]) + '<br> Adjusted R<sup>2</sup> = '
                                     + str(rfinder[1]),
                       showarrow=False,
                       xshift=1000,
                       yshift=-100)
    fig.show()

    print(results)


# Testing code
if __name__ == '__main__':
    # import python_ta.contracts
    #
    # python_ta.contracts.DEBUG_CONTRACTS = False
    # python_ta.contracts.check_all_contracts()
    #
    # import doctest
    #
    # doctest.testmod()
    #
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'disable': ['R1729', 'C0412'],
    #     'extra-imports': ['pandas', 'classes', 'plotly.express'],
    #     'max-line-length': 100
    # })
    industries = ["Agriculture, forestry, fishing and hunting", "Mining, quarrying, and oil and gas extraction",
                  "Construction", "Manufacturing", "Wholesale trade", "Retail trade",
                  "Transportation and warehousing",
                  "Information and cultural industries", "Finance and insurance",
                  "Real estate and rental and leasing",
                  "Professional, scientific and technical services", "Educational services",
                  "Administrative and support, waste management and remediation services",
                  "Health care and social assistance", "Arts, entertainment and recreation",
                  "Accommodation and food services", "Other services except public administration"]
    a = [classes.Industry(x) for x in industries]
    b = convert_to_dataframe(a)
    display_linear_graphs(b)
    display_linear_graphs(b, 'Revenue')
    display_linear_graphs(b, 'Lay Off Percentages')
