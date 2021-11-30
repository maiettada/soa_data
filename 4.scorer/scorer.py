import json
import spacy
from spacy.scorer import Scorer
from spacy.training import Example


gold_json1_filename = 'gold.json1'
labelled_json1_filename_regex = 'regex.json1'
labelled_json1_filename_spacy = 'spacy.json1'
output_scores_regex = 'scores_regex.json'
output_scores_spacy = 'scores_spacy.json'


def to_output_file(strings, filename):
    with open(filename, 'w') as a_file:
        for string in strings:
            a_file.write(string)
    return

def handle_outputs():
    import warnings
    warnings.filterwarnings("ignore")
    return


def unify_json_element(results_cat, results_class, list_name):
    return_list = dict(list(results_cat['ents_per_type'].items()) + list(results_class['ents_per_type'].items()))
    return {list_name: return_list}


def overlaps(interv_1, interv_2):
    overlapping = False
    if interv_2[1] - interv_1[0] > 0:
        if interv_1[1] - interv_2[0] > 0:
            overlapping = True
    return overlapping


def load_json_line_gold(gold_obj_json):
    """
    converting json string to json-inner-data-representation
    """

    gold_obj = json.loads(gold_obj_json)
    return gold_obj


def format_json_line_data_gold(gold_obj):
    """handling just json-data-structures"""

    loaded_gold_data = [[item.get('text'), item.get('labels'), item.get('meta').get('ord_id')] for item in gold_obj]
    return loaded_gold_data


def load_json_line_labelled(labelled_obj_json):
    """converting json string to json-inner-data-representation"""

    labelled_obj = json.loads(labelled_obj_json)
    return labelled_obj


def format_json_line_data_labelled(labelled_obj):
    """handling just json-data-structures"""

    loaded_labelled_data = [[item.get('labels'), item.get('meta').get('ord_id')] for item in labelled_obj]
    return loaded_labelled_data


def init_nlp():
    nlp = spacy.blank("it")
    nlp.add_pipe("ner")
    nlp.begin_training()
    return nlp


def selection_list(label_list_i, gold_annots, label_subcategory, approach=3):
    """
    Approaches developed to conduct the evaluation.
    Naive: just consider every label -> wrong labels require a try catch
    Strict: just consider labels that coincide with golden ones (exception-SAFE, Spacy will not raise errors)
    Loose approach: tolerate imprecise intervals; tolerate intervals with double-labels

    :param label_list_i:
    :param gold_annots:
    :param label_subcategory:
    :param approach:
    :return: list of labels to be considered
    """

    if approach == 1:
        label_list_i_naive_approach = [[start_offset, end_offset, word]
                                       for [start_offset, end_offset, word]
                                       in label_list_i
                                       if word in label_subcategory]
        return label_list_i_naive_approach
    elif approach == 2:
        label_list_i_strict_approach = [[start_offset, end_offset, word]
                                        for [start_offset, end_offset, word]
                                        in label_list_i
                                        if [start_offset, end_offset, word] in gold_annots
                                        if word in label_subcategory]
        return label_list_i_strict_approach
    elif approach == 3:
        used = []
        label_list_i_loose_approach = [[gold_start_offset, gold_end_offset, word]
                                       for [start_offset, end_offset, word] in label_list_i
                                       for [gold_start_offset, gold_end_offset, gold_word] in gold_annots
                                       if overlaps([start_offset, end_offset], [gold_start_offset, gold_end_offset])
                                       and [gold_start_offset, gold_end_offset, word] not in used
                                       and (used.append([gold_start_offset, gold_end_offset, word]) or True)
                                       ]
        return label_list_i_loose_approach


def evaluate(ner_model, gold_annotations, labelled_data_lines, label_subcategory):
    """
    Evaluates the goodness of the labelled data
    Evaluation is limited to the labels belonging to label_subcategory
    False positives are not taken into account by the scorer

    :param: ner_model that is used to create docs
    :param: gold_annotations, i.e. our ground truth
    :param: labelled_data_lines, i.e. the data to be evaluated
    :return: label_subcategory list, the list of labels to be considered in the evaluation
    (so allowing independent evaluations on different labels lists )
    """
    num_labels=0
    scorer = Scorer(ner_model)
    list = []
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
        label_list_i = [[s_o, e_o, label] for [s_o, e_o, label] in label_list_i if label in label_subcategory]
        num_labels = num_labels + len(label_list_i)
        gold_annots = [[s_o, e_o, label] for [s_o, e_o, label] in gold_annots if label in label_subcategory]
        labelled_ner_textunit = ner_model.make_doc(gold_textunit)
        label_list_i_selection = selection_list(label_list_i, gold_annots, label_subcategory)
        spans_i = [labelled_ner_textunit.char_span(start_offset, end_offset, word)
                   for [start_offset, end_offset, word] in label_list_i_selection]
        labelled_ner_textunit.ents = []
        added_spans = []
        for span_i_j in spans_i:
            try:
                added_spans.append(span_i_j)
                labelled_ner_textunit.ents = added_spans
            except:
                added_spans.remove(span_i_j)
            pass
        item = Example.from_dict(labelled_ner_textunit, {"entities": [[start_offset, end_offset, word]
                                                                      for [start_offset, end_offset, word]
                                                                      in gold_annots]})
        list.append(item)
    scores = scorer.score(list)
    print("numlabels", num_labels)
    return scores


def load_json_line_list(json1_filename):
    """
    converts jsonl file into list of json objects

    :param: jsonl filepath
    :return: list of json objects
    """

    labelled_obj_list = []
    with open(json1_filename, "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            labelled_obj_i = json.loads(stripped_line)
            labelled_obj_list.append(labelled_obj_i)
    return labelled_obj_list


def load_from_file(labelled_json1_filename):
    """
    Returns the contents of the gold file and the labelled file.

    :return: [json_line_list_gold, json_line_list_labelled], that are json lists respectively listing lines of the
    "gold_json1" file and the "labelled_json1" file
    """

    json_line_list_gold = load_json_line_list(gold_json1_filename)
    json_line_list_labelled = load_json_line_list(labelled_json1_filename)
    return [json_line_list_gold, json_line_list_labelled]


def format_data(file_data):
    """
    Formats gold-labels and labels as follows:
     - gold  = [ ['I like Europe and ice-creams.', [(7, 13, 'GPE'),(18,28,'food')]],   ...]
     - labelled  = [ [(7, 13, 'GPE')],  ...]

    :param: file_data, that is a list with file_data_gold labels and file_data_labelled labels
    :return: [gold, labelled]
    """

    file_data_gold = file_data[0]
    file_data_labelled = file_data[1]
    gold = format_json_line_data_gold(file_data_gold)
    labelled = format_json_line_data_labelled(file_data_labelled)
    return [gold, labelled]


def compute_score(labelled_json1_filename, output_filename):
    """
    Main part: aim of the script is to evaluate a labelling system by comparing its results to the given ground truth

    labelled_json1_filename: labelled file to be evaluated; here 3 regex with increasing complexity were used for SOA data;
                             regex-extracted SOA data are in v1.json1, v2.json1, v3.json1;
    gold_json1_filename: the ground truth;
    output_filename: file where the results of the evaluation are going to be written.

    to try with more easy json1 documents, do
    git checkout 283828b3b47dec37c3fa66c5284d02e61aa5289e -- gold.json1 labelled.json1
    and use the following line
    labelled_json1_filename = 'labelled.json1'
    """
    handle_outputs()
    ner_model = init_nlp()
    file_data = load_from_file(labelled_json1_filename)
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
    results = [None, None]
    """
    core part of the script: the evaluation, that is called twice:
     once for soa-categories, once for soa-classifications; result is sent in output to file
    """
    #for label_subcategory in evaluation_subcategory_lists:
    #    results[evaluation_subcategory_lists.index(label_subcategory)] = evaluate(ner_model, loaded_gold_data,
    #                                                                              loaded_labelled_data, label_subcategory)
    results_cat = evaluate(ner_model, loaded_gold_data, loaded_labelled_data, soa_categorie)
    results_class = evaluate(ner_model, loaded_gold_data, loaded_labelled_data, soa_classifiche)
    results_unified = unify_json_element(results_cat, results_class, 'ents_per_type')
    to_output_file(json.dumps(results_unified), output_filename)


if __name__ == "__main__":
    compute_score(labelled_json1_filename_regex, output_scores_regex)
    compute_score(labelled_json1_filename_spacy, output_scores_spacy)
