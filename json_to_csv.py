import json
from soa_data import *
import pandas as pd

pd.__version__

labels = soa_categorie + soa_classifiche


def fill_columns(labels, col_1, col_2, col_3):
    df = pd.DataFrame({
                       'Labels': labels,
                       'Regex P': col_1,
                       'Regex R': col_2,
                       'Regex F': col_3
                       })
    return df


def write_df(filepath, df):
    df.to_csv(filepath)


def write_to_csv(filepath, df):
    write_df(filepath, df)
    return

def make_ordered_list(entities, ordering_list):
    ordered_list = []
    for e in ordering_list:
        if e in ents_per_type:
            ordered_list.append([e, ents_per_type[e]['p'], ents_per_type[e]['r'], ents_per_type[e]['f']])
        else:
            ordered_list.append([e, "None", "None", "None"])
    return ordered_list

with open('json-results/result1-regex-soa-categories.json', 'r') as fp:
    line = fp.readline()
    json_elements = json.loads(line) #load-string line
    ents_per_type = json_elements['ents_per_type']
    ordered = make_ordered_list(ents_per_type, soa_categorie_valide)
with open('json-results/result1-regex-soa-classification.json', 'r') as fp:
    line = fp.readline()
    json_elements = json.loads(line) #load-string line
    ents_per_type = json_elements['ents_per_type']
    ordered = ordered + make_ordered_list(ents_per_type, soa_classifiche)
    keys =  [x[0] for x in ordered ]
    values_p = [x[1] for x in ordered]
    values_r = [x[2] for x in ordered]
    values_f = [x[3] for x in ordered]
    df = fill_columns(keys, values_p, values_r, values_f )
    write_to_csv('soa_os_og_regex.csv', df)
    write_to_csv('soa_os_og_full_automa.csv', df)
    write_to_csv('soa_os_og_full_rnd.csv', df)
    write_to_csv('soa_os_og_partial.csv', df)
