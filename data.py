"""

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Danesh Kohina, Enfei Zhang, Eric Shi, Jefferson Liu
"""
import datetime as dt


def is_float(element: str) -> bool:
    """Function to check if the string can be converted into a float

    """
    try:
        float(element)
        return True
    except ValueError:
        return False


def read_industry_csv_file(filename: str) -> dict[str: list[int]]:
    """Returns a dictionary of industries, with the name of the industry as the key and its appropriate data as a list

    The return value is a dictionary consisting of:

    - The key is the name of the industry
    - THe values are a list of the distributions under each section

    Preconditions:
      - filename refers to a valid csv file with data concerning industries
    """
    final_data = {}
    industries = ["Agriculture, forestry, fishing and hunting", "Mining, quarrying, and oil and gas extraction",
                  "Construction", "Manufacturing", "Wholesale trade", "Retail trade", "Transportation and warehousing",
                  "Information and cultural industries", "Finance and insurance", "Real estate and rental and leasing",
                  "Professional, scientific and technical services", "Educational services",
                  "Administrative and support, waste management and remediation services",
                  "Health care and social assistance", "Arts, entertainment and recreation",
                  "Accommodation and food services", "Other services"]
    clean_temp = []
    with open(filename) as file:
        temp = file.readlines()

    for line in temp:
        if any([industry in line for industry in industries]):
            clean_temp.append(line.split("\""))

    for item in clean_temp:
        count = sum([1 for x in item if x == ','])
        for _ in range(count):
            item.remove(",")
        count = sum(1 for x in item if x == "\n")
        for _ in range(count):
            item.remove("\n")
        count = sum(1 for x in item if x == "")
        for _ in range(count):
            item.remove("")
        temp_string = ""
        temp_list = []
        for char in item[0]:
            if ord(char) == 32 or ord(char) == 44 or 65 <= ord(char) <= 90 or 97 <= ord(char) <= 122:
                temp_string += char
        for x in range(1, len(item)):
            temp_num = ""
            for char in item[x]:
                if ord(char) == 46 or 48 <= ord(char) <= 57:
                    temp_num += char
            if is_float(temp_num):
                temp_list.append(float(temp_num))
            else:
                temp_list.append(0)
        temp_string = temp_string[:-2]
        final_data[temp_string] = temp_list
    return final_data


def read_company_csv_file(revenue_filename: str, shareprice_filename: str) -> list[float, float, float, float]:
    """Return

    """
    covid_start = dt.date(2020, 3, 1)
    final_data = []
    with open(revenue_filename) as file:
        temp_data = file.readlines()

    clean_temp = []
    pre_covid_revenue = 0
    post_covid_revenue = 0

    for line in range(len(temp_data) - 1):
        temp_list = []
        temp = temp_data[line].split('\"')
        temp_date = temp[0].split('/')
        clean_temp_date = []
        for value in temp_date:
            temp_num = ''
            for char in value:
                if 48 <= ord(char) <= 57:
                    temp_num += char
            clean_temp_date.append(temp_num)
        temp_list.append(dt.date(int(clean_temp_date[2]), int(clean_temp_date[0]), int(clean_temp_date[1])))
        temp_value = ''
        for char in temp[1]:
            if ord(char) == 46 or 48 <= ord(char) <= 57:
                temp_value += char
        temp_list.append(float(temp_value))
        clean_temp.append(temp_list)

    count = 0
    for rev in clean_temp:
        if rev[0] < covid_start:
            pre_covid_revenue += rev[1]
            count += 1
        else:
            post_covid_revenue += rev[1]

    final_data.append(pre_covid_revenue/count)
    final_data.append(post_covid_revenue/(len(clean_temp) - count))

    with open(shareprice_filename) as file:
        temp_data = file.readlines()

    clean_temp = []
    pre_covid_share = 0
    post_covid_share = 0

    for x in range(1, len(temp_data)):
        temp_list = []
        temp = temp_data[x].split(',')
        temp_date = temp[0].split('/')
        temp_list.append(dt.date(int(temp_date[2]), int(temp_date[0]), int(temp_date[1])))
        for y in range(1, len(temp)):
            temp_value = ''
            for char in temp[y]:
                if ord(char) == 46 or 48 <= ord(char) <= 57:
                    temp_value += char
            temp_list.append(float(temp_value))
        clean_temp.append(temp_list)

    count = 0
    for share in clean_temp:
        if share[0] < covid_start:
            pre_covid_share += (share[1] + share[3] + share[4] + share[5])/4
            count += 1
        else:
            post_covid_share += (share[1] + share[3] + share[4] + share[5]) / 4

    final_data.append(pre_covid_share/count)
    final_data.append(post_covid_share/(len(clean_temp) - count))
    return final_data
