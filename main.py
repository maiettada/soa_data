import json
import pickle

import spacy
from spacy.scorer import Scorer
from spacy.training import Example
from spacy.training import offsets_to_biluo_tags

gold_json1_filename = 'gold.json1'
labelled_json1_filename = 'v3.json1'
output_filename='output_file.txt'


def to_output_file(strings):
    with open(output_filename, "a") as a_file:
        for string in strings:
            a_file.write(string)
    return


def handle_outputs():
    import warnings
    warnings.filterwarnings("ignore")
    return


def overlaps(interv_1, interv_2):
    overlapping = False
    if interv_2[1] - interv_1[0] > 0:
        if interv_1[1] - interv_2[0] > 0:
            overlapping = True
    return overlapping


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


def init_nlp():
    nlp = spacy.blank("en")
    nlp.add_pipe("ner")
    nlp.begin_training()
    return nlp


def evaluate(ner_model, gold_annotations, labelled_data_lines, label_subcategory):
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
        label_list_i = [[s_o,e_o,label] for [s_o,e_o,label] in label_list_i if label in label_subcategory]
        gold_annots = [[s_o,e_o,label] for [s_o,e_o,label] in gold_annots if label in label_subcategory]
        labelled_ner_textunit = ner_model.make_doc(gold_textunit)
        used = []
        label_list_i_loose_approach = [[gold_start_offset, gold_end_offset, word]
                                       for [start_offset, end_offset, word] in label_list_i
                                       for [gold_start_offset, gold_end_offset, gold_word] in gold_annots
                                       if overlaps([start_offset, end_offset], [gold_start_offset, gold_end_offset])
                                       and [gold_start_offset, gold_end_offset, word] not in used
                                       and (used.append([gold_start_offset, gold_end_offset, word]) or True)
                                       ]
        spans_i = [labelled_ner_textunit.char_span(start_offset, end_offset, word)
                   for [start_offset, end_offset, word] in label_list_i_loose_approach]
        labelled_ner_textunit.ents = []
        added_spans = []
        for span_i_j in spans_i:
            try:
                added_spans.append(span_i_j)
                labelled_ner_textunit.ents = added_spans
            except TypeError:
                added_spans.remove(span_i_j)
            pass
        item = Example.from_dict(labelled_ner_textunit, {"entities": [[start_offset, end_offset, word]
                                                                      for [start_offset, end_offset, word]
                                                                      in gold_annots]})
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
    # return load_pickle_data()
    # json line: it's a full JSON  of a jsonl file.
    # In this context, a json line is related to an entire document
    # return [load_json_line_gold(gold_obj_json_string), load_json_line_labelled(labelled_obj_json_string)] #for json-list encoded in string
    json_line_list_gold = load_json_line_list(gold_json1_filename)
    json_line_list_labelled = load_json_line_list(labelled_json1_filename)
    return [json_line_list_gold, json_line_list_labelled]


def format_data(file_data):
    """"
    INTERFACE
     - gold_data = [ ['I like Europe and ice-creams.', [(7, 13, 'GPE'),(18,28,'food')]],
                    ...]
     - labelled_data = [ [(7, 13, 'GPE')],
                    ...]
    returns [gold_data, labelled_data]
    """
    # return file_data
    file_data_gold = file_data[0]
    file_data_labelled = file_data[1]
    gold = format_json_line_data_gold(file_data_gold)
    labelled = format_json_line_data_labelled(file_data_labelled)
    return [gold, labelled]

handle_outputs()
ner_model = init_nlp()
file_data = load_from_file()
[loaded_gold_data, loaded_labelled_data] = format_data(file_data)
# print(ner_model.pipe_names)
soa_classifiche = ['I', 'II', 'III-bis', 'IV', 'IV-bis', 'V', 'VI', 'VII', 'VIII']
soa_categorie = ['OG-1', 'OG-2', 'OG-3', 'OG-4', 'OG-5', 'OG-6', 'OG-7', 'OG-8', 'OG-9', 'OG-10',
                 'OG-11', 'OG-12', 'OG-13', 'OS-1', 'OS-2A', 'OS-2B', 'OS-3', 'OS-4', 'OS-5', 'OS-6',
                 'OS-7', 'OS-8', 'OS-9', 'OS-10', 'OS-11', 'OS-12A', 'OS-12B', 'OS-13',
                 'OS-14', 'OS-15', 'OS-16', 'OS-17', 'OS-18A', 'OS-18B', 'OS-19', 'OS-20A',
                 'OS-20B', 'OS-21', 'OS-22', 'OS-23', 'OS-24', 'OS-25', 'OS-26', 'OS-27',
                 'OS-28', 'OS-29', 'OS-30', 'OS-31', 'OS-32', 'OS-33', 'OS-34', 'OS-35']
evaluation_subcategory_lists = [soa_categorie, soa_classifiche]
results = [None,None]
for label_subcategory in evaluation_subcategory_lists:
    results[evaluation_subcategory_lists.index(label_subcategory)] = evaluate(ner_model, loaded_gold_data, loaded_labelled_data, label_subcategory)
for label_subcategory in evaluation_subcategory_lists:
    to_output_file(str(label_subcategory) +
                   " results\n: " +
                   str(results[evaluation_subcategory_lists.index(label_subcategory)]) +
                   "\n\n")
