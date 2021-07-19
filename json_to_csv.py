import json
from soa_data import *
import pandas as pd

pd.__version__

label_subset_os_og_categories = soa_categorie
label_subset_classes = soa_classifiche


def fill_columns(col_1, col_2):
    df = pd.DataFrame({'Colonna 1': col_1,
                       'colonna 2': col_2
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
    keys=[x for x in json_elements.keys()]
    values = [x for x in json_elements.values()]
    df = fill_columns(keys, values )
    write_to_csv('soa_os_og.csv', list(json_elements.keys()), label_subset_os_og_categories, df)
