"""

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Danesh Kohina, Enfei Zhang, Eric Shi, Jefferson Liu
"""
from dataclasses import dataclass


@dataclass
class Industry:
    """Dataclass of relevant industry information including layoff percentage, total layoffs, expenses and revenue

    Instance Attributes:
      - name: the name of the industry
      - layoffPercentages: the distributions of the percentage of people laid off in the industry
      - layoffTotals: the distribution of the total amount of people laid off in the industry
      - expenses: the distribution of the expenses of companies in the industry
      - revenue: the distribution of the revenue of companies in the industry

    Representation Invariants:
        - self.name != ''
        - all(0 <= p <= 100 for p in self._layoffPercentages)
        - all(0 <= p <= 100 for p in self._layoffTotals)
        - all(0 <= p <= 100 for p in self._expenses)
        - all(0 <= p <= 100 for p in self._revenue)
    """
    name: str
    layoffPercentages: dict[int]
    layoffTotals: dict[int]
    expenses: dict[int]
    revenue: dict[int]


class Company:
    """
    Dataclass of relevant company information

    Attributes
    - market_cap: the market cap of the company pre covid
    - revenue: the quarterly revenue of the company pre covid
    - industry: the industry the company is in

    Representation Invariants:
      - self.name != ''
      - self.market_cap >= 0
      - self.revenue >= 0
      - self.industry.name != ''

    Sample Usage:
    >>> pre_covid_apple = Company(market_cap = 87935000000, revenue = 247417000000, industry = 'Technology')
    """
    _name: str
    _market_cap: float
    _revenue: float
    _industry: Industry

    def __init__(self, name: str, cap: float, revenue: float, industry: Industry = None) -> None:
        """

        """
        self._name = name
        self._market_cap = cap
        self._revenue = revenue
        if industry is not None:
            self._industry = industry
        else:
            self._industry = self.find_industry()

    def find_industry(self) -> Industry:
        """Finds the industry the company is in

        """

    def calculate_vulnerability_value(self) -> float:
        """Calculates the vulnerability of the company

        """

        return self
