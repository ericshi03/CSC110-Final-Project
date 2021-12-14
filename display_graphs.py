"""
TODO: ADD UNITS TO THE VALUES

This file will take in data and using the plotly, pandas, and statsmodels class, will output
a graph of the inputted relation with an analysis being printed as well.
"""
import pandas
import plotly.express as px
import classes
from typing import Optional


def convert_to_dataframe(values: list[classes.Industry]):
    """
    This function will convert the list of Industries into a dataframe.
    """
    names = []
    lay_off_per_avg = []
    revenue_avg = []
    expenses_avg = []
    vuln_val = []
    for val in values:
        names.append(val.name)
        lay_off_per_avg.append(sum(val.layoffPercentages) / len(val.layoffPercentages))
        revenue_avg.append(val.revenue[0])
        expenses_avg.append(val.expenses[0])
        vuln_val.append(val.vulnerability)
    processed_values = {'Industries': names, 'Lay Off Percentages': lay_off_per_avg, 'Revenue': revenue_avg,
                        'Expenses': expenses_avg, 'Vulnerability Values': vuln_val}
    return pandas.DataFrame(data=processed_values)


def display_linear_graphs(df: pandas.DataFrame, factor: Optional[str] = 'Expenses') -> None:
    """
    This function will take in a DataFrame class and will output a graph based on the factor
    specified.


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
                                     + str(rfinder[0]) + '<br> Adjusted R<sup>2</sup> = ' + str(rfinder[1]),
                       showarrow=False,
                       xshift=1000,
                       yshift=-100)
    fig.show()

    print(results)


if __name__ == '__main__':
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
