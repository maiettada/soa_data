import spacy
from contextlib import contextmanager
import sys, os
import pandas as pd
import json
soa_csv_fp = 'Dataset/soa.csv'
jsonl_file = 'spacy_ner.json1'


def print_to_file(json_line):
    """
    This function writes data df to a file
    """
    with open(jsonl_file, 'a') as f:
        f.write(json_line)
        f.write('\n')



def dumps_labels_only(retr, array_index):
    #with suppress_stdout():
    #    empty_excluded = exclude_empty_sublist(retr)
    #   return json.dumps({"meta": {"ord_id": array_index, "fr_id": 0},
    #                  "labels": json_with_postprocessed_data(empty_excluded)})
    return json.dumps({"meta": {"ord_id": array_index, "fr_id": 0},
                        "labels": retr})


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def read_df(filepath, section):
    with suppress_stdout():
        dataframe = pd.read_csv(filepath, sep=',')
        return dataframe[section]


def use_model(index):
    # Use a breakpoint in the code line below to debug your script.
    testi = read_df(soa_csv_fp, 'testo')
    document = testi[index]
    nlp = spacy.load("./output/model-last")
    doc = nlp(document)
    json_like = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
    print(doc.ents)
    print(json_like)
    return json_like


def interval_doc_dump():
    """
    Executing the regex soa-extraction on an interval of docs.
    """
    start_index = 0
    end_index = 100
    for indice in range(start_index, end_index):
        with suppress_stdout():
             retr = use_model(indice)
        # print(dumps_jsonl(text, retr, indice))
        print_to_file(dumps_labels_only(retr, indice))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    interval_doc_dump()

