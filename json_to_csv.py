import json
from soa_data import *
import pandas as pd

pd.__version__

labels = soa_categorie_valide + soa_classifiche


def fill_columns(labels, col_1, col_2, col_3):
    """
    This function builds a Pandas Dataframe using the columns col_1, col_2, col_3

    :rtype: pandas dataframe built with the columns data
    """
    df = pd.DataFrame({
        'Labels': labels,
        'Regex P': col_1,
        'Regex R': col_2,
        'Regex F': col_3
    })
    return df


def write_to_csv(filepath, df):
    """

    :param filepath: file csv to be written
    :param df:  table data (Pandas dataframe)
    """
    df.to_csv(filepath)


def make_ordered_list(entities, ordering_list):
    """
    This function:
    1.takes the "entities" key/value pairs;
    2. follows the key-order given by ordering list
    3. outputs a list of numbers, sorted by the ordering_list, adding "none" whenever there was no value for a specified key

    :param entities: example entities=["os-3": 0.3, "os-2": 0.2, "os-1": 0.1]
    :param ordering_list: example ordering_list=["os-1","os-2","os-3","os-4","os-5"]
    :return: example [ 0.1, 0.2, 0.3, "None", "None"]
    """
    ordered_list = []
    for e in ordering_list:
        if e in entities.keys():
            ordered_list.append([e, entities[e]['p'], entities[e]['r'], entities[e]['f']])
        else:
            ordered_list.append([e, "None", "None", "None"])
    return ordered_list


def json_results_to_csv(json_filepath, csv_filepath):
    """
    Aim of the function:
    1.extracting the key/values from ents_per_type json_array
    2.putting them in the right order
    3.writing them to a csv file
    """

    with open(json_filepath, 'r') as fp:
        json_elements = json.load(fp)  # load-string line
        ents_per_type = json_elements['ents_per_type']
        ordered = make_ordered_list(ents_per_type, labels)
        keys = [x[0] for x in ordered]
        values_p = [x[1] for x in ordered]
        values_r = [x[2] for x in ordered]
        values_f = [x[3] for x in ordered]
        df = fill_columns(keys, values_p, values_r, values_f)
        write_to_csv(csv_filepath, df)
    return


"""
Aim of this part:
1.extracting the key/values from ents_per_type json_array
2.putting them in the right order (first categories, then classifications)
3.writing them to a csv file

note: json_results_to_csv does the same, but here I don't use that because I have two different jsons-files with data
to be merged 
"""
with open('json-results/result1-regex-soa-categories.json', 'r') as fp:
    line = fp.readline()
    json_elements = json.loads(line)  # load-string line
    ents_per_type = json_elements['ents_per_type']
    ordered = make_ordered_list(ents_per_type, soa_categorie_valide)
with open('json-results/result1-regex-soa-classification.json', 'r') as fp:
    line = fp.readline()
    json_elements = json.loads(line)  # load-string line
    ents_per_type = json_elements['ents_per_type']
    ordered = ordered + make_ordered_list(ents_per_type, soa_classifiche)
    keys = [x[0] for x in ordered]
    values_p = [x[1] for x in ordered]
    values_r = [x[2] for x in ordered]
    values_f = [x[3] for x in ordered]
    df = fill_columns(keys, values_p, values_r, values_f)
    write_to_csv('csv_tables/soa_os_og_regex.csv', df)
json_results_to_csv('json-results/result2-full-automa.json', 'csv_tables/soa_os_og_full_automa.csv')
json_results_to_csv('json-results/result3-full-rnd.json', 'csv_tables/soa_os_og_full_rnd.csv')
json_results_to_csv('json-results/result4-partial-sentences.json', 'csv_tables/soa_os_og_partial.csv')
