import spacy
import random
import json
from spacy.training import Example


def init_nlp():
    nlp = spacy.blank("en")
    nlp.add_pipe("ner")
    nlp.begin_training()
    return nlp


def list_examples(ner_model, gold_annotations):
    list = []
    i = 0
    for [gold_textunit, gold_annots] in gold_annotations:
        labelled_ner_textunit = ner_model(gold_textunit)
        '''spans = [ labelled_ner_textunit.char_span(start_offset, end_offset, word) for [start_offset, end_offset, word] in label_list_i ]
        labelled_ner_textunit.ents = spans'''
        item = Example.from_dict(labelled_ner_textunit, {"entities": gold_annots})
        list.append(item)
    return list


TRAINING_DATA = gold_data = [
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and Africa and chocolate.',
     [(7, 13, 'GPE'), (18, 24, 'GPE'),(29,38,'food')]],
    ['I like Europe and Africa and Japan.',
     [(7, 13, 'GPE'), (18, 24, 'GPE'), (29, 34, 'GPE')]]
]

print(TRAINING_DATA)

ner_model = init_nlp()
list = list_examples(ner_model,TRAINING_DATA)
losses = ner_model.update(list)
print(losses)
