import spacy
from spacy.training import Example
from spacy.scorer import Scorer


def evaluate(ner_model, examples):
    scorer = Scorer(ner_model)
    gold_list = []
    for input_, annot in examples:
        doc_gold_text = ner_model.make_doc(input_)
        gold = Example.from_dict(doc_gold_text, {"entities": annot})
        gold_list.append(gold)
        pred_value = ner_model(input_)
    scores = scorer.score(gold_list)
    return scores

# example run

examples = [
    ('Who is Shaka Khan?',
     [(7, 17, 'PERSON')]),
    ('I like London and Berlin.',
     [(7, 13, 'LOC'), (18, 24, 'LOC')])
]

#ner_model = spacy.load(ner_model_path) # for spaCy's pretrained use 'en_core_web_sm'

ner_model = spacy.load('en_core_web_sm')
results = evaluate(ner_model, examples)