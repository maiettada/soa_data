import json
from soa_data import *
import pandas as pd

pd.__version__

label_subset_os_og_categories = soa_categorie
label_subset_classes = soa_classifiche


def fill_columns(labels, col_1, col_2, col_3):
    df = pd.DataFrame({
                       'Labels': labels,
                       'Colonna 1': col_1,
                       'colonna 2': col_2,
                       'colonna 3': col_3
                       })
    return df


def write_df(filepath, df):
    df.to_csv(filepath)


def write_to_csv(filepath, list_items, label_subset_classes, df):
    write_df(filepath, df)
    return


col_1 = [2, 4, 6, 8, 10]
with open('evaluations-three-line.json1', 'r') as fp:
    line = fp.readline()
    json_elements = json.loads(line) #load-string line
    ents_per_type = json_elements['ents_per_type']
    keys=[x for x in ents_per_type.keys()]
    #values = [x for x in ents_per_type.values()]
    values_p = [x['p'] for x in ents_per_type.values()]
    values_r = [x['r'] for x in ents_per_type.values()]
    values_f = [x['f'] for x in ents_per_type.values()]
    df = fill_columns(keys, values_p, values_r, values_f )
    write_to_csv('soa_os_og.csv', list(json_elements.keys()), label_subset_os_og_categories, df)

