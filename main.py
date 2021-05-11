import json
import pickle

import spacy
from spacy.scorer import Scorer
from spacy.training import Example

gold_json1_filename = 'gold.json1'

labelled_json1_filename = 'labelled.json1'

gold_obj_json_string = '[\
    {"text": "I like Europe and ice-creams.","meta": {"ord_id": 1, "fr_id": 0}, "labels": [[7, 13, "GPE"],[18,28,"food"]]},\
    {"text": "I like Europe and ice-creams.","meta": {"ord_id": 2, "fr_id": 0}, "labels": [[7, 13, "GPE"],[18,28,"food"]]},\
    {"text": "I like Europe and ice-creams.","meta": {"ord_id": 4, "fr_id": 0}, "labels": [[7, 13, "GPE"],[18,28,"food"]]}\
]'

labelled_obj_json_string = '[\
    {"meta": {"ord_id": 1, "fr_id": 0}, "labels": [[7, 13, "GPE"],[18,28,"food"]]},\
    {"meta": {"ord_id": 2, "fr_id": 0}, "labels": [[7, 13, "GPE"]]},\
    {"meta": {"ord_id": 3, "fr_id": 0}, "labels": [[7, 13, "GPE"]]}\
]'


def load_json_line_gold(gold_obj_json):
    '''converting json string to json-inner-data-representation'''
    gold_obj = json.loads(gold_obj_json)
    return gold_obj


def format_json_line_data_gold(gold_obj):
    '''handling just json-data-structures'''
    loaded_gold_data = [[item.get('text'), item.get('labels'), item.get('meta').get('ord_id')] for item in gold_obj]
    return loaded_gold_data


def load_json_line_labelled(labelled_obj_json):
    '''converting json string to json-inner-data-representation'''
    labelled_obj = json.loads(labelled_obj_json)
    return labelled_obj


def format_json_line_data_labelled(labelled_obj):
    '''handling just json-data-structures'''
    loaded_labelled_data = [[item.get('labels'), item.get('meta').get('ord_id')] for item in labelled_obj]
    return loaded_labelled_data


produce_annotation_files_gold_data = [
    ['I like Europe and ice-creams.', [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and Africa and chocolate.', [(7, 13, 'GPE'), (18, 24, 'GPE'),(29,38,'food')]],
    ['I like Europe and Africa and Japan.', [(7, 13, 'GPE'), (18, 24, 'GPE'), (29, 34, 'GPE')]]
]
produce_annotation_files_labelled_data = [
    [(7, 13, 'GPE')],
    [(7, 13, 'GPE'),(18,24, 'GPE'),(29,38,'food')],
    [(7, 13, 'GPE'),(18,24, 'GPE')]
]

def init_nlp():
    nlp = spacy.blank("en")
    nlp.add_pipe("ner")
    nlp.begin_training()
    return nlp


def evaluate(ner_model, gold_annotations, labelled_data_lines):
    scorer = Scorer(ner_model)
    list = []
    i = 0
    for [gold_textunit, gold_annots, gold_ord_id] in gold_annotations:
        if not labelled_data_lines:
            label_list_i = []
        else:
            label_list_i_enclosed = [labelled_data_line_objects[0] for labelled_data_line_objects in labelled_data_lines
                            if labelled_data_line_objects[1] == gold_ord_id]
            if label_list_i_enclosed:
                label_list_i = label_list_i_enclosed[0]
            else:
                label_list_i = []
        labelled_ner_textunit = ner_model.make_doc(gold_textunit)
        spans = [ labelled_ner_textunit.char_span(start_offset, end_offset, word) for [start_offset, end_offset, word] in label_list_i ]
        labelled_ner_textunit.ents = spans
        item = Example.from_dict(labelled_ner_textunit, {"entities": gold_annots})
        list.append(item)
    scores = scorer.score(list)
    return scores

def load_json_line_list(json1_filename):
    '''converting jsonl file (string made of lines of json) into list of json objects'''
    labelled_obj_list = []
    with open(json1_filename, "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            labelled_obj_i = json.loads(stripped_line)
            labelled_obj_list.append(labelled_obj_i)
    return labelled_obj_list


def load_from_file():
    #return load_pickle_data()
    # json line: it's a full JSON  of a jsonl file.
    # In this context, a json line is related to an entire document
    #return [load_json_line_gold(gold_obj_json_string), load_json_line_labelled(labelled_obj_json_string)] #for json-list encoded in string
    return [load_json_line_list(gold_json1_filename), load_json_line_list(labelled_json1_filename)]


def format_data(file_data):
    """"
    INTERFACE
     - gold_data = [ ['I like Europe and ice-creams.', [(7, 13, 'GPE'),(18,28,'food')]],
                    ...]
     - labelled_data = [ [(7, 13, 'GPE')],
                    ...]
    returns [gold_data, labelled_data]
    """
    #return file_data
    file_data_gold = file_data[0]
    file_data_labelled = file_data[1]
    gold = format_json_line_data_gold(file_data_gold)
    labelled = format_json_line_data_labelled(file_data_labelled)
    return [gold, labelled]


ner_model = init_nlp()
file_data = load_from_file()
[loaded_gold_data, loaded_labelled_data] = format_data(file_data)
print(ner_model.pipe_names)
results = evaluate(ner_model, loaded_gold_data, loaded_labelled_data)
print(results)








