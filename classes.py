"""
Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Danesh Kohina, Enfei Zhang, Eric Shi, Jefferson Liu
"""
from dataclasses import dataclass
import data as dt


@dataclass
class Industry:
    """Dataclass of relevant industry information including layoff percentage, total layoffs, expenses and revenue
    Instance Attributes:
      - name: the name of the industry
      - layoffPercentages: the distributions of the percentage of people laid off in the industry
      - expenses: the distribution of the expenses of companies in the industry
      - revenue: the distribution of the revenue of companies in the industry
    Representation Invariants:
        - self.name != ''
        - all(0 <= p <= 100 for p in self._layoffPercentages)
        - all(0 <= p <= 100 for p in self._expenses)
        - all(0 <= p <= 100 for p in self._revenue)
    """
    name: str
    layoffPercentages: list[int]
    expenses: list[int]
    revenue: list[int]
    vulnerability: float

    def __init__(self, ind: str) -> None:
        """
        """
        self.name = ind
        key = ""
        industries = ["Agriculture, forestry, fishing and hunting", "Mining, quarrying, and oil and gas extraction",
                      "Construction", "Manufacturing", "Wholesale trade", "Retail trade",
                      "Transportation and warehousing",
                      "Information and cultural industries", "Finance and insurance",
                      "Real estate and rental and leasing",
                      "Professional, scientific and technical services", "Educational services",
                      "Administrative and support, waste management and remediation services",
                      "Health care and social assistance", "Arts, entertainment and recreation",
                      "Accommodation and food services", "Other services except public administration"]
        for industry in industries:
            if str.upper(self.name) in str.upper(industry):
                key = industry
        self.layoffPercentages = dt.read_industry_csv_file("3310025201-eng.csv")[key]
        self.expenses = dt.read_industry_csv_file("3310028201-eng.csv")[key]
        self.revenue = dt.read_industry_csv_file("3310028101-eng.csv")[key]
        self.vulnerability = self.calculate_industry_vulnerability()

    def calculate_industry_vulnerability(self) -> float:
        """Calculates the vulnerability value of the industry


        """
        average_layoff = 0
        for value in self.layoffPercentages:
            if value != max(self.layoffPercentages):
                average_layoff += value
        layoff_vulnerability = (self.layoffPercentages.index(max(self.layoffPercentages)) + 1 * max(
            self.layoffPercentages) / 10) + average_layoff / 11
        rev_exp_vuln = ((self.revenue[0] - (self.revenue[3] - self.revenue[2])) + (
                self.expenses[0] - (self.expenses[3] - self.expenses[2]))) / 1000
        temp_vuln = (rev_exp_vuln + layoff_vulnerability + layoff_vulnerability * rev_exp_vuln) / 2
        return temp_vuln


class Company:
    """
    Dataclass of relevant company information
    Attributes
    - name: the name of the company
    - share_price: the share price of the company pre covid
    - revenue: the quarterly revenue of the company pre covid
    - industry: the industry the company is in

    Representation Invariants:
      - self.name != ''
      - self.share_price >= 0
      - self.revenue >= 0
      - self.industry.name != ''

    Sample Usage:
    >>> pre_covid_apple = Company(87935000000, 247417000000,  'Technology')
    """
    _name: str
    _share_price_post_covid: float
    _share_price_pre_covid: float
    _revenue_post_covid: float
    _revenue_pre_covid: float
    _industry: Industry

    def __init__(self, name: str, share_post: float, share_pre: float, revenue_post: float, revenue_pre: float,
                 industry: str) -> None:
        """
        """
        self._name = name
        self._share_price_post_covid = share_post
        self._share_price_pre_covid = share_pre
        self._revenue_post_covid = revenue_post
        self._revenue_pre_covid = revenue_pre
        self._industry = Industry(industry)

    def calculate_vulnerability_value(self) -> float:
        """Calculates the vulnerability of the company
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
