#tratto da https://course.spacy.io/en/chapter4
from spacy.matcher import Matcher
from spacy.lang.en import English

def create_training_data():
    TEXTS = ['How to preorder the iPhone X', 'iPhone X is coming', 'Should I pay $1,000 for the iPhone X?',
             'The iPhone 8 reviews are here', "iPhone 11 vs iPhone 8: What's the difference?",
             'I need a new phone! Any tips?']

    nlp = English()
    matcher = Matcher(nlp.vocab)

    def on_match(matcher, doc, id, matches):
        print('Matched!', matches)

    patterns = [
       [{"LOWER": "iphone"}, {"LOWER": "x"}],
       [{"LOWER": "iphone"}, {"IS_DIGIT": True}]
    ]
    matcher.add("TEST_PATTERNS", patterns, on_match=on_match)

    TRAINING_DATA = []
    # Create a Doc object for each text in TEXTS
    for doc in nlp.pipe(TEXTS):
        # Match on the doc and create a list of matched spans
        spans = [doc[start:end] for match_id, start, end in matcher(doc)]
        # Get (start character, end character, label) tuples of matches
        entities = [(span.start_char, span.end_char, "GADGET") for span in spans]
        # Format the matches as a (doc.text, entities) tuple
        training_example = (doc.text, {"entities": entities})
        # Append the example to the training data
        TRAINING_DATA.append(training_example)

    print(*TRAINING_DATA, sep="\n")
    return TRAINING_DATA

create_training_data()

'''
nlp.pipe(VETTORE_DI_TESTI) 

alternativa scalabile delle due righe seguenti

doc_i = nlp(testo_i) #esamina testo i-esimo
matches = matcher(doc_i) #stampa matches del testo i-esimo
'''