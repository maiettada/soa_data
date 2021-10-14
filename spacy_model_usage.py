import spacy
from spacy.tokens import DocBin

nlp = spacy.load("./training/UD_English-EWT/model-last")
doc_bin = DocBin().from_disk("./corpus/UD_English-EWT/test.spacy")
docs = list(doc_bin.get_docs(nlp.vocab))
text = docs[0]
print(text.text)
doc = nlp(text.text)
print(doc.ents)
