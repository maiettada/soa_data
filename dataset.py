import random
import spacy
import json
from spacy.tokens import DocBin

nlp = spacy.blank("it")
train = DocBin()
dev = DocBin()
test = DocBin()

with open('gold.json1', 'r') as fp:
    for line in fp.readlines():
        random_value = random.random()
        item = json.loads(line)
   
        #TODO
        #crea un nuovo documento: ogni documento è derivato da una frase
        #period_sect
        doc = nlp.make_doc(item['text'])

        entities = []
        
        # legge le etichette
        for label in item['labels']:
            # label[0] -> carattere di inizio
            # label[1] -> carattere di fine
            # label[2] -> nome dell'etichetta
            span = doc.char_span(label[0], label[1], label=label[2], alignment_mode="contract")
            entities.append(span)

        try:
            # prova ad assegnare le etichette al documento
            doc.ents = entities
        except:
            # se fallisce perché le etichette non sono valide ignora il documento
            continue

        #TODO
        #sostituisci il random_value con l'automaton_value
        # E SE UNA FRASE AVESSE PIÙ DI UNA LABEL?
        # I approccio: vale la decisione di una delle labels(la prima??per semplicità)
        # II approccio: boh, fare complesse valutazioni contando le decisioni di un tipo e di un altro
        #               priorità alta alla decisione "train", media alla decisione "test", bassa alla decisione "dev"
        if random_value < 0.7:
            # 70% degli esempi nel training set
            train.add(doc)
        elif random_value < 0.8:
            # 10% degli esempi nel dev set
            dev.add(doc)
        else:
            # 20% degli esempi nel test set
            test.add(doc)

train.to_disk("./train.spacy")
dev.to_disk("./dev.spacy")
test.to_disk("./test.spacy")
