"""

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Danesh Kohina, Enfei Zhang, Eric Shi, Jefferson Liu
"""


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
        count = sum([1 for x in item if x == ","])
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


def read_company_csv_file(filename: str) -> list:
    return []
