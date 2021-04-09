import spacy
from spacy.training import Example
from spacy.scorer import Scorer

def init_nlp():
    nlp = spacy.blank("en")
    nlp.add_pipe("ner")
    nlp.begin_training()
    return nlp


def evaluate(ner_model, gold_examples, labelled_span):
    scorer = Scorer(ner_model)
    list = []
    i = 0
    for input_, gold_annot in gold_examples:
        label_list = labelled_span[i]
        if i<len(labelled_span):
            i = i+1
        doc_under_evaluation = ner_model.make_doc(input_)
        spans = [ doc_under_evaluation.char_span(label[0], label[1], label="GPE") for label in label_list]
        doc_under_evaluation.ents = spans
        pred_value = ner_model(input_)
        print([(ent.text, ent.label_) for ent in pred_value.ents])
        item = Example.from_dict(doc_under_evaluation, {"entities": gold_annot})
        list.append(item)
    scores = scorer.score(list)
    return scores

# example run

gold_data = [
    ('I like Europe.',
     [(7, 13, 'GPE')]),
    ('I like Europe and Africa.',
     [(7, 13, 'GPE'), (18, 24, 'GPE')]),
    ('I like Europe and Africa and Japan.',
     [(7, 13, 'GPE'), (18, 24, 'GPE'),(29,34, 'GPE')])
]

labelled_data = [
    [(7, 13)],
    [(7, 13),(18,24)],
    [(7, 13),(18,24)]
]

ner_model = init_nlp()
print(ner_model.pipe_names)
results = evaluate(ner_model, gold_data, labelled_data)
print(results)
