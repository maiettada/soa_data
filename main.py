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
        print(pred_value)
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

ner_model = spacy.load('en_core_web_lg')
results = evaluate(ner_model, examples)
print(results)

'''
    UAS (Unlabelled Attachment Score) and LAS (Labelled Attachment Score) are standard
     metrics to evaluate dependency parsing. UAS is the proportion of tokens whose head has been correctly assigned,
      LAS is the proportion of tokens whose head has been correctly assigned with the right 
      dependency label (subject, object, etc).
    ents_p, ents_r, ents_f are the precision, recall and fscore for the NER task.
    tags_acc is the POS tagging accuracy.
    token_acc seems to be the precision for token segmentation.


    2
    To add on, ents_p, ents_r and ents_f are calculated based on per entity basis. 
    That is to say spaCy considers all entities in your document(s) to find true positive,
     false positive and false negative. 
     I had an initial impressive that so long an predicted entity in a sentence matches the gold set,
      it would +1 to the true positive count but I was wrong. 
      For those interested to dig in, do look into language.py, scorer.py and evaluate.py 
      to run through the calculations. – Derek Chia Nov 15 '18 at 5:14

'''