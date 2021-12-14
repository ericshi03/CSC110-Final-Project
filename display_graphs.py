"""
Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Danesh Kohina, Enfei Zhang, Eric Shi, Jefferson Liu

This file will take in data and use the plotly, statsmodel, and pandas modules to
graphically represent the correlation between our calculated risk factor and a factor
of our choosing.

Author: Eric Shi
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
        lay_off_per_avg.append(sum(val.lay_off_percentages) / len(val.lay_off_percentages))
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
    import python_ta

    python_ta.check_all(config={
        'disable': ['R1729', 'C0412'],
        'allowed-io': ['display_linear_graphs'],
        'extra-imports': ['pandas', 'classes', 'plotly.express'],
        'max-line-length': 100
    })
