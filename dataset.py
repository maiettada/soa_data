import random
import spacy
import json
from spacy.tokens import DocBin

from distribution_automaton import DistributionAutomaton
from dataset_division import *

nlp = spacy.blank("it")
train = DocBin()
dev = DocBin()
test = DocBin()

from distribution_automaton import DistributionAutomaton

soa_classifiche = ['I', 'II', 'III-bis', 'IV', 'IV-bis', 'V', 'VI', 'VII', 'VIII']
soa_categorie = ['OG-1', 'OG-2', 'OG-3', 'OG-4', 'OG-5', 'OG-6', 'OG-7', 'OG-8', 'OG-9', 'OG-10',
                 'OG-11', 'OG-12', 'OG-13', 'OS-1', 'OS-2A', 'OS-2B', 'OS-3', 'OS-4', 'OS-5', 'OS-6',
                 'OS-7', 'OS-8', 'OS-9', 'OS-10', 'OS-11', 'OS-12A', 'OS-12B', 'OS-13',
                 'OS-14', 'OS-15', 'OS-16', 'OS-17', 'OS-18A', 'OS-18B', 'OS-19', 'OS-20A',
                 'OS-20B', 'OS-21', 'OS-22', 'OS-23', 'OS-24', 'OS-25', 'OS-26', 'OS-27',
                 'OS-28', 'OS-29', 'OS-30', 'OS-31', 'OS-32', 'OS-33', 'OS-34', 'OS-35', '']
label_list = soa_categorie + soa_classifiche
# creating object of the class
obj_list = []
for label in label_list:
    new_obj = DistributionAutomaton(label)
    obj_list.append(new_obj)
'''
for obj in obj_list:
    print(obj.get_label())
    print(obj.read_decision())
'''

# tested with gold-debug.json1 = {"id": 71379, "text": "nel paese di OS7 e OS8.", "labels": [[13, 16, "OS-7"], [19, 22, "OS-8"]]}


with open('gold-debug.json1', 'r') as fp:
    sentences_labels_list = []
    for line in fp.readlines():
        item = json.loads(line)
        txt_base = item['text']
        json_list_base = item['labels']
        sort_list(json_list_base)
        found = 0
        while found != -1:
            # crea un nuovo documento: ogni documento è derivato da una frase
            found, json_list_base, txt_base = period_sect(json_list_base, txt_base, sentences_labels_list)
        #END OF PREPROCESSING
    for txt, json_list in sentences_labels_list:
        doc = nlp.make_doc(txt)
        entities = []
        train_decided = False
        test_decided = False
        # legge le etichette
        if not json_list:
            for obj in obj_list:
                if obj.get_label() == "":
                    break;
            decision = obj.read_decision('1')
            if decision == DistributionAutomaton.train_decision:
                train_decided = True
            elif decision == DistributionAutomaton.test_decision:
                test_decided = True
            else:
                # implicitly dev_decided= True
                pass
        else:
            for label in json_list:
                # label[0] -> carattere di inizio
                # label[1] -> carattere di fine
                # label[2] -> nome dell'etichetta
                span = doc.char_span(label[0], label[1], label=label[2], alignment_mode="contract")
                entities.append(span)
                try:
                    # prova ad assegnare le etichette al documento
                    doc.ents = entities
                    print(doc.ents)
                    for obj in obj_list:
                        if obj.get_label()==label[2]:
                            break; #assuming json files are using correct labels!!
                    decision = obj.read_decision('1')
                    if decision == DistributionAutomaton.train_decision:
                        train_decided = True
                    elif decision == DistributionAutomaton.test_decision:
                        test_decided = True
                    else:
                        #implicitly dev_decided= True
                        pass
                except:
                    # se fallisce perché le etichette non sono valide ignora il documento
                    continue
        #sostituisci il random_value con l'automaton_value
        # E SE UNA FRASE AVESSE PIÙ DI UNA LABEL?
        # I approccio: vale la decisione di una delle labels(la prima??per semplicità)
        # II approccio: priorità alta alla decisione "train", media alla decisione "test", bassa alla decisione "dev"
        if train_decided:
            # 70% degli esempi nel training set
            train.add(doc)
        elif test_decided:
            # 20% degli esempi nel test set
            test.add(doc)
        else:
            # 10% degli esempi nel dev set
            dev.add(doc)

train.to_disk("./train.spacy")
dev.to_disk("./dev.spacy")
test.to_disk("./test.spacy")

