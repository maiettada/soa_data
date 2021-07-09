import spacy
import json
from spacy.tokens import DocBin
from dataset_division import period_sect,sort_list
from distribution_automaton import DistributionAutomaton
from soa_data import soa_classifiche, soa_categorie


def read_json1_and_sect_by_period(fp, sentences_labels_list):
    """

    :param fp:
    :param sentences_labels_list:
    :return:
    """
    for line in fp.readlines():
        item = json.loads(line)
        txt_base = item['text']
        json_list_base = item['labels']
        sort_list(json_list_base)
        found = 0
        while found != -1:
            # crea un nuovo documento: ogni documento è derivato da una frase
            found, json_list_base, txt_base = period_sect(json_list_base, txt_base, sentences_labels_list)
        # END OF PREPROCESSING
    return


def retrieve_obj_by_label(label: str):
    """

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


def add_to_decided_bin(doc, train, dev, test, train_decided, test_decided, train_documentation, dev_documentation, test_documentation, labels_list, appending_to_test_list):
    """
    The procedure assigns a doc to the proper train/dev/test DocBin; since train/dev/test doc-bins need a 70% - 10 % - 20% of the label instances,
    for every label an automaton object decided "train" or "test" ( or other, i.e. dev).
    The doc can have more than one labels, so the decision is the following:
    train_decide flag True, the doc with all its labels is sent to the "train" doc-bin;
    test_decide flag False, then the test_decide flag could send the doc+labels to the "test" doc-bin;
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
        # 70% degli esempi nel training set
        train.add(doc)
        if appending_to_test_list:
            train_documentation.append(labels_list)
        print("train bin will get labels: ", labels_list)
    elif test_decided:
        # 20% degli esempi nel test set
        test.add(doc)
        if appending_to_test_list:
            test_documentation.append(labels_list)
        print("test bin will get labels: ", labels_list)
    else:
        # 10% degli esempi nel dev set
        dev.add(doc)
        if appending_to_test_list:
            dev_documentation.append(labels_list)
        print("dev bin will get labels: ", labels_list)
    return


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
    if not labels_list:
        obj = retrieve_obj_by_label("")
        obj.label_increase()
        decision = obj.read_decision()
        train_decided, test_decided = decide_for_single_label(decision, train_decided, test_decided)
        '''        
        add_to_decided_bin(doc, train, dev, test, train_decided, test_decided, train_documentation, dev_documentation,
                           test_documentation, unsafe_entities_local_debug, True)
            '''
    else:
        # legge le etichette
        print()
        print("(json_list)", '\n', labels_list)
        #decide for empty json_list
        for label_element in labels_list:
            # label_element[0] -> carattere di inizio
            # label_element[1] -> carattere di fine
            # label_element[2] -> nome dell'etichetta
            span = doc.char_span(label_element[0], label_element[1], label=label_element[2], alignment_mode="contract")
            unsafe_entities_local.append(span)
            unsafe_entities_local_debug.append(label_element)
            try:
                # prova ad assegnare le etichette al documento
                #PREFERISCO far scoppiare l'errore sulla singola ultima label
                doc.ents = unsafe_entities_local
                # decisione ( prima era sopra al try)
                obj = retrieve_obj_by_label(label_element[2])
                obj.label_increase()
                decision = obj.read_decision()
                train_decided, test_decided = decide_for_single_label(decision, train_decided, test_decided, label_element[2])
                print("ok - stored into safe")
                # sostituisco l'approccio random_value con l'automaton_value
                # E SE UNA FRASE AVESSE PIÙ DI UNA LABEL?
                # I approccio: vale la decisione di una delle labels(la prima??per semplicità)
                # II approccio: priorità alta alla decisione "train", media alla decisione "test", bassa alla decisione "dev"
                if label_element[2]=='OS-30':
                    print("very close")
            except:
                # se fallisce: l'ultima delle etichette di json_list non era valida
                # si espelle l'ultima etichetta, si arresta l'elaborazione di json_list
                unsafe_entities_local.pop()
                unsafe_entities_local_debug.pop()
                doc.ents = unsafe_entities_local
                print("exception- forgetting problematic label")
        add_to_decided_bin(doc, train, dev, test, train_decided, test_decided, train_documentation, dev_documentation,
                           test_documentation, unsafe_entities_local_debug, True)

    return


def process_json1(obj_list, train, dev, test, train_documentation, test_documentation, dev_documentation):
    """
    The procedure reads a json1 file, then calls the read_json1_and_sect_by_period.
    Finally, it distributes each sentence and related labels to the proper bin.

    :param obj_list: lists of labels-automataxxx
    :param train: train DocBin
    :param dev: dev DocBin
    :param test: test DocBin
    :param train_documentation: (for debugging purposes) will contain labels-lists that are added into train docbin;
    :param test_documentation: (for debugging purposes) will contain labels-lists that are added into test docbin;
    :param dev_documentation: (for debugging purposes) will contain labels-lists that are added into dev docbin;
    :return:
    """
    with open('gold-debug.json1', 'r') as fp:
        sentences_labels_list = []
        read_json1_and_sect_by_period(fp, sentences_labels_list)
        # now sentences_labels_list has the pairs (txt, json_list)
        # to be initialised once initially
        for txt, json_list in sentences_labels_list:
            # to be initialised for every couple (txt, json_list)
            if json_list: #just for debugging: TO BE REMOVED
                decide_where_to_put(txt, json_list, train_documentation, dev_documentation, test_documentation)
    return



nlp = spacy.blank("it")
train = DocBin()
dev = DocBin()
test = DocBin()
train_documentation = []
test_documentation = []
dev_documentation = []
soa_values_list = soa_categorie + soa_classifiche
# creating object of the class
obj_list = []
for label in soa_values_list:
    new_obj = DistributionAutomaton(label)
    obj_list.append(new_obj)
# tested with gold-debug.json1 = {"id": 71379, "text": "nel paese di OS7 e OS8.", "labels": [[13, 16, "OS-7"], [19, 22, "OS-8"]]}
process_json1(obj_list, train, dev, test, train_documentation, test_documentation, dev_documentation)
train.to_disk("./train.spacy")
dev.to_disk("./dev.spacy")
test.to_disk("./test.spacy")


