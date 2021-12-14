"""CSC110 Final Project Classes file

File Description
================
This file contains the necessary classes to find the vulnerability of a company/industry

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of anyone who wishes to use it.
All forms of distribution of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2021 Danesh Kohina, Enfei Zhang, Eric Shi, Jefferson Liu
"""
import data as dt


class Industry:
    """A custom data type that represents industry information including
    layoff percentage, total layoffs, expenses and revenue

    Instance Attributes:
      - name: the name of the industry
      - lay_off_percentages: the distributions of the percentage of people laid off in the industry
      - expenses: the expenses of companies in the industry averaged by quartiles
      - revenue: the revenues of companies in the industry averaged by quartiles

    Representation Invariants:
        - self.name != ''
        - all(0 <= p <= 100 for p in self.lay_off_percentages)
        - all(0 <= p for p in self.expenses)
        - all(0 <= p for p in self.revenue)
    """
    name: str
    lay_off_percentages: list[float]
    expenses: list[float]
    revenue: list[float]
    vulnerability: float

    def __init__(self, ind: str) -> None:
        """
        Initializes a new Industry object
        """
        self.name = ind
        key = ""
        industries = ['Agriculture, forestry, fishing and hunting',
                      'Mining, quarrying, and oil and gas extraction',
                      'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade',
                      'Transportation and warehousing',
                      'Information and cultural industries', 'Finance and insurance',
                      'Real estate and rental and leasing',
                      'Professional, scientific and technical services', 'Educational services',
                      'Administrative and support, waste management and remediation services',
                      'Health care and social assistance', 'Arts, entertainment and recreation',
                      'Accommodation and food services',
                      'Other services except public administration']
        for industry in industries:
            if str.upper(self.name) in str.upper(industry):
                key = industry
        self.lay_off_percentages = dt.read_industry_csv_file('3310025201-eng.csv')[key]
        self.expenses = dt.read_industry_csv_file('3310028201-eng.csv')[key]
        self.revenue = dt.read_industry_csv_file('3310028101-eng.csv')[key]
        self.vulnerability = self.calculate_industry_vulnerability()

    def calculate_industry_vulnerability(self) -> float:
        """Calculates the vulnerability value of the industry

        Preconditions:
        - self.lay_off_percentages is not None
        - self.expenses is not None
        - self.revenue is not None

        Sample Usage:
        >>> import math
        >>> Agriculture = Industry("Agriculture")
        >>> math.isclose(Agriculture.calculate_industry_vulnerability(), 8.426045363636366)
        True
        """
        average_layoff = 0
        for value in self.lay_off_percentages:
            if value != max(self.lay_off_percentages):
                average_layoff += value
        layoff_vulnerability = (self.lay_off_percentages.index(max(self.lay_off_percentages))
                                + 1 * max(self.lay_off_percentages) / 10) + average_layoff / 11
        rev_exp_vuln = ((self.revenue[0] - (self.revenue[3] - self.revenue[2]))
                        + (self.expenses[0] - (self.expenses[3] - self.expenses[2]))) / 1000
        temp_vuln = (rev_exp_vuln + layoff_vulnerability + layoff_vulnerability * rev_exp_vuln) / 2
        return temp_vuln


class Company:
    """
    A custom data type that represents company information including name,
    share price pre & post covid, revenue pre & post covid and the industry it's in

    Instance Attributes:
    - name: the name of the company
    - share_price_post_covid: the share price of the company post covid
    - share_price_pre_covid: the share price of the company pre covid
    - revenue_post_covid: the quarterly revenue of the company post covid
    - revenue_pre_covid: the quarterly revenue of the company pre covid
    - industry: the industry the company is in

    Representation Invariants:
      - self._name != ''
      - self._share_price_post_covid >= 0
      - self._share_price_pre_covid >= 0
      - self._revenue_post_covid >= 0
      - self._revenue_pre_covid >= 0
      - self._industry.name != ''
    """
    _name: str
    _share_price_post_covid: float
    _share_price_pre_covid: float
    _revenue_post_covid: float
    _revenue_pre_covid: float
    _industry: Industry

    def __init__(self, name: str, data: list[float, float, float, float], industry: str) -> None:
        """
        Initialize a new Company object
        """
        self._name = name
        self._share_price_post_covid = data[0]
        self._share_price_pre_covid = data[1]
        self._revenue_post_covid = data[2]
        self._revenue_pre_covid = data[3]
        self._industry = Industry(industry)

    def calculate_vulnerability_value(self) -> float:
        """Calculates the vulnerability value of the industry

        Preconditions:
        - self._share_price_post_covid is not None
        - self._share_price_pre_covid is not None
        - self._revenue_post_covid is not None
        - self._revenue_pre_covid is not None
        - self._industry is not None

        Sample Usage:
        >>> import math
        >>> Farmville = Company("Farmville", 25, 30, 200000, 190000, "Agriculture")
        >>> math.isclose(Farmville.calculate_vulnerability_value(), 196.41131383767754)
        True
        """
        total_mc = self._share_price_pre_covid + self._share_price_post_covid
        total_r = self._revenue_pre_covid + self._revenue_post_covid

        difference_in_mc = abs(self._share_price_pre_covid - self._share_price_post_covid)
        percentage_change_in_mc = difference_in_mc / (total_mc / 2) * 100

        difference_in_r = abs(self._revenue_pre_covid - self._revenue_post_covid)
        percentage_change_in_r = difference_in_r / (total_r / 2) * 100

        vulnerability = percentage_change_in_mc + percentage_change_in_r
        vulnerability *= self._industry.vulnerability
        return vulnerability


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['python_ta.contracts', 'math', 'data'],
        'disable': ['R1705', 'C0200'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
