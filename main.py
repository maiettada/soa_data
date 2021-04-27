import spacy
from spacy.training import Example
from spacy.scorer import Scorer
import pickle

def produce_annotation_files():
    gold_data = [
    ['I like Europe and ice-creams.',
     [(7, 13, 'GPE'),(18,28,'food')]],
    ['I like Europe and Africa and chocolate.',
     [(7, 13, 'GPE'), (18, 24, 'GPE'),(29,38,'food')]],
    ['I like Europe and Africa and Japan.',
     [(7, 13, 'GPE'), (18, 24, 'GPE'), (29, 34, 'GPE')]]
    ]
    labelled_data = [
    [(7, 13, 'GPE')],
    [(7, 13, 'GPE'),(18,24, 'GPE'),(29,38,'food')],
    [(7, 13, 'GPE'),(18,24, 'GPE')]
    ]
    with open('gold.pickle', 'wb') as f:
        pickle.dump(gold_data, f)
    with open('labelled.pickle', 'wb') as f:
        pickle.dump(labelled_data, f)

def init_nlp():
    nlp = spacy.blank("en")
    nlp.add_pipe("ner")
    nlp.begin_training()
    return nlp


def evaluate(ner_model, gold_annotations, labelled_data_list):
    scorer = Scorer(ner_model)
    list = []
    i = 0
    for input_textunit_, gold_annot in gold_annotations:
        if labelled_data_list:
            label_list_i = labelled_data_list[i]
            if i + 1 < len(labelled_data_list):
                i = i + 1
        else:
            label_list_i = []
        labelled_ner_textunit = ner_model.make_doc(input_textunit_)
        spans = [ labelled_ner_textunit.char_span(label[0], label[1], label[2]) for label in label_list_i]
        labelled_ner_textunit.ents = spans
        item = Example.from_dict(labelled_ner_textunit, {"entities": gold_annot})
        list.append(item)
    scores = scorer.score(list)
    return scores


#produce_annotation_files() #used once to produce external files
ner_model = init_nlp()
with open('gold.pickle', 'rb') as f:
    loaded_gold_data = pickle.load(f)
    print(loaded_gold_data)
with open('labelled.pickle', 'rb') as f:
    loaded_labelled_data = pickle.load(f)
    print(loaded_labelled_data)
print(ner_model.pipe_names)
results = evaluate(ner_model, loaded_gold_data, loaded_labelled_data)
print(results)
