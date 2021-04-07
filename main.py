import spacy
from spacy.training import Example
from spacy.scorer import Scorer
from spacy.tokens import Doc
from spacy.tokens import Span
from spacy.matcher import Matcher
from spacy.lang.en import English


def on_match(matcher, doc, id, matches):
    print('Matched!', matches)
    pass

def create_training_data():
    TEXTS = ['I like Europe.',
             'I went to Scandinavia',
             ]
    nlp = English()
    matcher = Matcher(nlp.vocab)
    patterns = [
        [{"LOWER": "europe"}],
        [{"LOWER": "scandinavia"}]
    ]
    matcher.add("TEST_PATTERNS", patterns, on_match=on_match)
    TRAINING_DATA = []
    # Create a Doc object for each text in TEXTS
    for doc in nlp.pipe(TEXTS):
        # Match on the doc and create a list of matched spans
        spans = [doc[start:end] for match_id, start, end in matcher(doc)]
        # Get (start character, end character, label) tuples of matches
        entities = [(span.start_char, span.end_char, "GPE") for span in spans]
        # Format the matches as a (doc.text, entities) tuple
        training_example = (doc.text, {"entities": entities})
        # Append the example to the training data
        TRAINING_DATA.append(training_example)
    # print(*TRAINING_DATA, sep="\n")
    return TRAINING_DATA


def train_nlp(TRAINING_DATA):
    # Create a blank "en" model
    nlp = spacy.blank("en")
    # Create a new entity recognizer and add it to the pipeline
    nlp.add_pipe("ner")
    # Add the label "GPE" to the entity recognizer
    # nlp.add_label("GPE")
    # Start the training
    nlp.begin_training()
    doc = Doc(nlp.vocab, words=["I", "like", "Europe","."])
    tags_ref = ["", "", "GPE",""]
    example = Example.from_dict(doc, {"tags": tags_ref})
    examples = []
    examples.append(example)
    nlp.update(examples)
    return nlp


def evaluate(ner_model, gold_examples, labelled_span):
    #ner_model = English()
    scorer = Scorer(ner_model)
    list = []
    i = 0
    for input_, gold_annot in gold_examples:
        label = labelled_span[i][0] # [0] just for vector data unboxing, beeing vector like it follows [(data)]
        if i<len(labelled_span):
            i = i+1
        doc_under_evaluation = ner_model.make_doc(input_)
        span = Span(doc_under_evaluation, label[0], label[1], label="GPE") #cosa il modello linguistico riconoscerebbe
        doc_under_evaluation.ents = [span]
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
    [(2, 3)],
    [(2, 3)],
    [(2, 3)]
]
#ner_model = spacy.load(ner_model_path) # for spaCy's pretrained use 'en_core_web_sm'
TRAINING_DATA = create_training_data()
ner_model = train_nlp(TRAINING_DATA)
print(ner_model.pipe_names)
# spacy.load('en_core_web_lg')
results = evaluate(ner_model, gold_data, labelled_data)
print(results)
