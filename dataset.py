import spacy
import json
from spacy.tokens import DocBin
from dataset_division import period_sect,sort_list
from distribution_automaton import DistributionAutomaton
from soa_data import soa_classifiche, soa_categorie


def read_json1_and_sect_by_period(fp, sentences_labels_list):
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
    for obj in obj_list:
        if obj.get_label() == label:
            break;
    return obj


def decide_for_single_label(decision, label_element=""):
    train_decided = False
    test_decided = False
    if decision == DistributionAutomaton.train_decision:
        train_decided = True
        print("train-decision for: ", label_element[2])
    elif decision == DistributionAutomaton.test_decision:
        test_decided = True
        print("test-decision for: ", label_element[2])
    else:
        # implicitly dev_decided= True
        print("dev-decision for: ", label_element[2])
    return train_decided, test_decided


unsafe_entities = []


def add_to_decided_bin(doc, train, dev, test, train_decided, test_decided, train_documentation, dev_documentation, test_documentation, json_list, appending_to_test_list):
    if train_decided:
        # 70% degli esempi nel training set
        train.add(doc)
        if appending_to_test_list:
            train_documentation.append(json_list)
        print("train bin will get json-list: ", json_list)
    elif test_decided:
        # 20% degli esempi nel test set
        test.add(doc)
        if appending_to_test_list:
            test_documentation.append(json_list)
        print("test bin will get json-list: ", json_list)
    else:
        # 10% degli esempi nel dev set
        dev.add(doc)
        if appending_to_test_list:
            dev_documentation.append(json_list)
        print("dev bin will get json-list: ", json_list)
    return


def decide_where_to_put(txt,json_list, train_documentation, dev_documentation, test_documentation):
    unsafe_entities_local = []
    doc = nlp.make_doc(txt)
    train_decided = False
    test_decided = False
    empty = False
    if not json_list:
        obj = retrieve_obj_by_label("")
        obj.label_increase()
        decision = obj.read_decision()
        train_decided, test_decided = decide_for_single_label(decision)
        '''
        #TO BE ADDED LATER
        if train_decided:
            # 70% degli esempi nel training set
            train.add(doc)
            train_documentation.append(json_list)
            print("train bin will get json-list: ", json_list)
        elif test_decided:
            # 20% degli esempi nel test set
            test.add(doc)
            test_documentation.append(json_list)
            print("test bin will get json-list: ", json_list)
        else:
            # 10% degli esempi nel dev set
            dev.add(doc)
            dev_documentation.append(json_list)
            print("dev bin will get json-list: ", json_list)
            '''
    else:
        # legge le etichette
        print()
        print("(json_list)", '\n', json_list)
        #decide for empty json_list
        for label_element in json_list:
            # label_element[0] -> carattere di inizio
            # label_element[1] -> carattere di fine
            # label_element[2] -> nome dell'etichetta
            span = doc.char_span(label_element[0], label_element[1], label=label_element[2], alignment_mode="contract")
            unsafe_entities_local.append(span)
            try:
                # prova ad assegnare le etichette al documento
                #PREFERISCO far scoppiare l'errore sulla singola ultima label
                doc.ents = unsafe_entities_local
                # decisione ( prima era sopra al try)
                obj = retrieve_obj_by_label(label_element[2])
                obj.label_increase()
                decision = obj.read_decision()
                train_decided, test_decided = decide_for_single_label(decision, label_element)
                print("ok - stored into safe")
                # sostituisci il random_value con l'automaton_value
                # E SE UNA FRASE AVESSE PIÙ DI UNA LABEL?
                # I approccio: vale la decisione di una delle labels(la prima??per semplicità)
                # II approccio: priorità alta alla decisione "train", media alla decisione "test", bassa alla decisione "dev"
                if label_element[2]=='OS-30':
                    print("very close")
            except:
                # se fallisce: l'ultima delle etichette di json_list non era valida
                # si espelle l'ultima etichetta, si arresta l'elaborazione di json_list
                unsafe_entities_local.pop()
                doc.ents = unsafe_entities_local
                print("exception- forgetting problematic label")
        add_to_decided_bin(doc, train, dev, test, train_decided, test_decided, train_documentation, dev_documentation,
                           test_documentation, json_list, True)

    return


def process_json1(obj_list, train, dev, test, train_documentation, test_documentation, dev_documentation):
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

'''
def is_list_passed_by_value(li):
    li.append("1")
    return


lis = []
for i in range(1,10):
    is_list_passed_by_value(lis)
    print(lis)
'''

nlp = spacy.blank("it")
train = DocBin()
dev = DocBin()
test = DocBin()
train_documentation = []
test_documentation = []
dev_documentation = []
label_list = soa_categorie + soa_classifiche
# creating object of the class
obj_list = []
for label in label_list:
    new_obj = DistributionAutomaton(label)
    obj_list.append(new_obj)
# tested with gold-debug.json1 = {"id": 71379, "text": "nel paese di OS7 e OS8.", "labels": [[13, 16, "OS-7"], [19, 22, "OS-8"]]}
process_json1(obj_list, train, dev, test, train_documentation, test_documentation, dev_documentation)
train.to_disk("./train.spacy")
dev.to_disk("./dev.spacy")
test.to_disk("./test.spacy")

