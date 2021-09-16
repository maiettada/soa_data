import spacy
import json
from spacy.tokens import DocBin
from dataset_division import period_level_section, sort_list
from distribution_automaton import DistributionAutomaton
from soa_data import soa_classifiche, soa_categorie
import random

"""
    This script creates the doc_bins needed by Spacy (train, dev, test) for the setup of a neural network(spacy "ner" 
    task).
    A ground truth must be given in input ( in variable gold_json1_file).
    The ground truth is read, with all the text and golden labels.
    Text and labels are divided in smaller docs, made by single sentences and related labels.
    At the end of the execution every (sentence, label) couple is sent to a doc_bin,
    either randomly ( random_strategy boolean, set by default)
    either with DistributionAutomaton that keeps track of the already-processed data.
"""


#input
gold_json1_file = 'gold.json1'

#output filepaths
train_docbin = "./train.spacy"
dev_docbin = "./dev.spacy"
test_docbin = "./test.spacy"


def read_json1_and_section_by_period(fp, sentences_labels_list, n_lines=-1):
    """
    preprocessing: this procedure takes the json1 file, reads each line;
    for each line, moreover, sectioning in sentences is executed to permit later analysis at sentence level.

    :param fp:
    :param sentences_labels_list: list to be filled with pairs ((sentence),[[label_1],[label_2]...[label_n]])
    :param n_lines: max #lines to be partitioned in sentences
    :return:
    """
    divide = True
    for line in fp.readlines():
        item = json.loads(line)
        txt_base = item['text']
        json_list_base = item['labels']
        sort_list(json_list_base)
        found = 0
        if n_lines > 0:
            n_lines = n_lines -1
            divide = True
        elif n_lines == 0:
            divide = False
        else:
            pass   #n_lines=-1, NO MAXIMUM
        while found != -1:
            # crea un nuovo documento: ogni documento è derivato da una frase
            found, json_list_base, txt_base = period_level_section(json_list_base, txt_base, sentences_labels_list, divide)
    return


def retrieve_obj_by_label(label: str):
    """
    Helper function to quickly select the automaton for the specified label

    :param label:
    :return:
    """
    for obj in obj_list:
        if obj.get_label() == label:
            break;
    return obj


def decide_for_single_label(decision, train_decided, test_decided, label=""):
    """
    Can raise the train_decided or the test_decided flag depending on the label-automaton decision boolean.

    :param decision: decision of the automaton related to the "label"
    :param train_decided
    :param test_decided
    :param label
    :return: train_decided, test_decided
    """
    if decision == DistributionAutomaton.train_decision:
        train_decided = True
        print("train-decision for: ", label)
    elif decision == DistributionAutomaton.test_decision:
        test_decided = True
        print("test-decision for: ", label)
    else:
        # implicitly dev_decided= True
        print("dev-decision for: ", label)
    return train_decided, test_decided


def add_to_decided_bin(doc, train, dev, test, train_decided, test_decided, train_documentation, dev_documentation,
                       test_documentation, labels_list, appending_to_test_list):
    """
    The procedure assigns a doc to the proper train/dev/test DocBin; since train/dev/test doc-bins need a 70% - 10 % - 20% of the label instances,
    for every label an automaton object decided "train" or "test" ( or other, i.e. dev).
    The doc can have more than one labels, so the decision is the following:
    train_decide has high priority; then, test_decide has medium priority; just
    if both train_decide and test_decide are false, then the doc is sent to the "dev" doc-bin.

    :param doc: spacy document data structure
    :param train: DocBin
    :param dev: DocBin
    :param test: DocBin
    :param train_decided: boolean flag to signal that at least one label was decided to be put to train DocBin
    :param test_decided: boolean flag to signal that at least one label was decided to be put to test DocBin
    :param train_documentation: (for debugging purposes) will contain labels-lists that are added into train docbin;
    :param test_documentation: (for debugging purposes) will contain labels-lists that are added into test docbin;
    :param dev_documentation: (for debugging purposes) will contain labels-lists that are added into dev docbin;
    :param labels_list: humar-readable labels_list (it can be added to the *_documentation lists)
    :param appending_to_test_list: debug condition for enabling the usage of the  *_documentation lists
    :return:
    """
    if train_decided:
        # 70% to the training set
        train.add(doc)
        if appending_to_test_list:
            train_documentation.append(labels_list)
        print("train bin will get labels: ", labels_list)
    elif test_decided:
        # 20% to the test set
        test.add(doc)
        if appending_to_test_list:
            test_documentation.append(labels_list)
        print("test bin will get labels: ", labels_list)
    else:
        # 10% to the dev set
        dev.add(doc)
        if appending_to_test_list:
            dev_documentation.append(labels_list)
        print("dev bin will get labels: ", labels_list)
    return


def make_unique_list(labels_list):
    used = []
    labels_consider_just_once = [x for x in labels_list if x not in used and (used.append(x) or True)]
    return labels_consider_just_once


def automata_decide_listwise(labels_list):
    train_decided, test_decided = [False, False]
    labels_list = [x[2] for x in labels_list]
    labels_consider_just_once = make_unique_list(labels_list)
    for label_string in labels_consider_just_once:
        obj = retrieve_obj_by_label(label_string)
        obj.label_increase()
        decision = obj.read_decision()
        train_decided, test_decided = decide_for_single_label(decision, train_decided, test_decided,
                                                              label_string)
    return train_decided, test_decided


def randomly_decide():
    random_value = random.random()
    train_decided, test_decided = False, False
    if random_value < 0.7:
        # 70% samples into training set
        train_decided = True
    elif random_value < 0.8:
        # 10% samples into training set dev set
        pass
    else:
        # 20% samples into training set test set
        test_decided = True
    return train_decided, test_decided


def decide_where_to_put(txt, labels_list, train_documentation, dev_documentation, test_documentation):
    """
    This function does two things:
    1. assigns doc.ents=span(label) for each label of the list, also taking care of the exceptions that could rise;
    2. decides whether to put the doc in train DocBin, test DocBin or dev DocBin

    :param txt: single sentence
    :param labels_list: labels related to the sentence "txt"
    :param train_documentation: (for debugging purposes) will contain labels-lists that are added into train docbin;
    :param test_documentation: (for debugging purposes) will contain labels-lists that are added into test docbin;
    :param dev_documentation: (for debugging purposes) will contain labels-lists that are added into dev docbin;
    :return:
    """
    unsafe_entities_local = []
    unsafe_entities_local_debug = []
    doc = nlp.make_doc(txt)
    train_decided = False
    test_decided = False
    labels_present = False
    if not labels_list:
        empty_label = ""
        labels_list= [[None, None, empty_label]]
        # recovered the lack of label by faking a "" label ( even docs without labels must be distributed to bins)
    else:
        labels_present = True
        print('\n', "(json_list)", '\n', labels_list)
        # decide for empty json_list
        for label_element in labels_list:
            span = doc.char_span(label_element[0],        # -> starting character
                                 label_element[1],        # -> ending character
                                 label=label_element[2],  # -> label
                                 alignment_mode="contract")
            unsafe_entities_local.append(span)
            unsafe_entities_local_debug.append(label_element)
            try:
                # here the error can arise
                doc.ents = unsafe_entities_local
            except:
                # last label is giving error; we just pop it
                unsafe_entities_local.pop()
                unsafe_entities_local_debug.pop()
                doc.ents = unsafe_entities_local
                print("exception- forgetting problematic label")
    if random_strategy:
        train_decided, test_decided = randomly_decide()
    else:
        train_decided, test_decided = automata_decide_listwise(labels_list)
    print("ok - stored into safe")
    add_to_decided_bin(doc, train, dev, test, train_decided, test_decided, train_documentation, dev_documentation,
                       test_documentation, unsafe_entities_local_debug, labels_present)
    return


def process_json1(ground_truth, obj_list, train, dev, test, train_documentation, test_documentation, dev_documentation):
    """
    The procedure reads a json1 file, then calls the read_json1_and_sect_by_period.
    Finally, it distributes each sentence and related labels to the proper bin.

    :param ground_truth: filepath(string) for json1 file with golden annotations
    :param obj_list: lists of labels-automataxxx
    :param train: train DocBin
    :param dev: dev DocBin
    :param test: test DocBin
    :param train_documentation: (for debugging purposes) will contain labels-lists that are added into train docbin;
    :param test_documentation: (for debugging purposes) will contain labels-lists that are added into test docbin;
    :param dev_documentation: (for debugging purposes) will contain labels-lists that are added into dev docbin;
    :return:
    """
    with open(ground_truth, 'r') as fp:
        sentences_labels_list = []
        read_json1_and_section_by_period(fp, sentences_labels_list, -1)  # -1: everything must be cut into sentences
        # now sentences_labels_list has the pairs (txt, json_list)
        for txt, json_list in sentences_labels_list:
            decide_where_to_put(txt, json_list, train_documentation, dev_documentation, test_documentation)
    return


def main():
    """
        train, dev, test: docbins where this script is going to put the docs.
        train_documentation, test_documentation, dev_documentation: lists where I put the labels, so I can check their
         distribution at debugging phase
        random/not random(DistributionAutomaton): alternatives for distributing labels

        Final output: *.spacy files to be used in the spacy training
    """
    random_strategy = True
    nlp = spacy.blank("it")
    train = DocBin()
    dev = DocBin()
    test = DocBin()
    train_documentation = []
    test_documentation = []
    dev_documentation = []
    soa_values_list = soa_categorie + soa_classifiche
    # creating objects of the class distributionAutomaton
    obj_list = []
    if not random_strategy:
        for label in soa_values_list:
            new_obj = DistributionAutomaton(label)
            obj_list.append(new_obj)
    # first test with gold.json1 = {"id": 71379, "text": "nel paese di OS7 e OS8.",
    # "labels": [[13, 16, "OS-7"], [19, 22, "OS-8"]]}
    process_json1(gold_json1_file, obj_list, train, dev, test, train_documentation, test_documentation, dev_documentation)
    if not random_strategy:
        print("total #values:", len(soa_values_list), "#labels activated: ",len([x.is_it_used() for x in obj_list if x.is_it_used()==True]))
        print("#completed distr in the automata documents: ",len([x.how_many_distributions() for x in obj_list
                                                                  if x.how_many_distributions() >= 1]))
        print([(x.get_label(), x.how_many_distributions()) for x in obj_list])
    train.to_disk(train_docbin)
    dev.to_disk(dev_docbin)
    test.to_disk(test_docbin)


if __name__ == "__main__":
    main()
