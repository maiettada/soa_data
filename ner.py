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
    for [gold_textunit, gold_annots] in gold_annotations:
        labelled_ner_textunit = ner_model(gold_textunit)
        '''spans = [ labelled_ner_textunit.char_span(start_offset, end_offset, word) for [start_offset, end_offset, word] in label_list_i ]
        labelled_ner_textunit.ents = spans'''
        item = Example.from_dict(labelled_ner_textunit, {"entities": gold_annots})
        list.append(item)
    return list


TRAINING_DATA = [

    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]]
]

print(TRAINING_DATA)
ner_model = init_nlp()
list = list_examples(ner_model,TRAINING_DATA)
losses = ner_model.update(list)
print(losses)


text='I like Europe and chocolate.'
# Process the text
doc = ner_model(text)

# Iterate over the entities
for ent in doc.ents:
    # Print the entity text and label
    print(ent.text, ent.start_char, ent.end_char, ent.label_)


# Loop for 10 iterations
for itn in range(3):
    # Shuffle the training data
    random.shuffle(TRAINING_DATA)
    losses = {}

    # Batch the examples and iterate over them
    for batch in spacy.util.minibatch(TRAINING_DATA, size=10):
        training = [ [text, entities] for text, entities in batch ]
        print(training)
        # Update the model
        list_2 = list_examples(ner_model, training)
        losses = ner_model.update(list_2)
    print(losses)

text='I like Europe and chocolate.'
# Process the text
doc = ner_model(text)

# Iterate over the entities
for ent in doc.ents:
    # Print the entity text and label
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
