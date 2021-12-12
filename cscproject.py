"""
This is my draft of the csc project. I want to essentially create the data scraper for all of the datasets

requirements
- datasets have to be all the same
- if they are not same, then I have to do other stuff that will make me sad.
"""

from dataclasses import dataclass
import industry
import csv


@dataclass
class Company:
    """
    Dataclass of relevant company information

    Attributes
    - market_cap: the market cap of the company pre covid
    - revenue: the quarterly revenue of the company pre covid
    - industry: the industry the company is in

    Representation Invariants:
      - self.market_cap >= 0
      - self.revenue >= 0
      - self.industry.name != ''

    Sample Usage:
    >>> pre_covid_apple = Company(market_cap = 87935000000, revenue = 247417000000, industry = 'Technology')
    """
