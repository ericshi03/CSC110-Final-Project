"""CSC110 Final Project Classes file

File Description
================
This file runs all our files and classes

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of anyone who wishes to use it.
All forms of distribution of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2021 Danesh Kohina, Enfei Zhang, Eric Shi, Jefferson Liu
"""
import data as dt
import classes
import display_graphs as dg

if __name__ == '__main__':
    nutrien_values = dt.read_company_csv_file('Company Datasets/agriculture/Nutrien/revenue.csv',
                                              'Company Datasets/agriculture/Nutrien/shareprice.csv')
    Nutrien = classes.Company('Nutrien', nutrien_values, 'Agriculture')
    print('The vulnerability value for Nutrien is ' + str(Nutrien.calculate_vulnerability_value()))

    industries = ['Agriculture, forestry, fishing and hunting', 'Mining, quarrying, and oil and gas extraction',
                  'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade',
                  'Transportation and warehousing',
                  'Information and cultural industries', 'Finance and insurance',
                  'Real estate and rental and leasing',
                  'Professional, scientific and technical services', 'Educational services',
                  'Administrative and support, waste management and remediation services',
                  'Health care and social assistance', 'Arts, entertainment and recreation',
                  'Accommodation and food services', 'Other services except public administration']
    a = [classes.Industry(x) for x in industries]
    b = dg.convert_to_dataframe(a)
    dg.display_linear_graphs(b)
