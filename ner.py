'''***************************************************************************************
Chapter 4: Training a neural network model

In this chapter, you'll learn how to update spaCy's statistical models to customize them for your use case – for example, to predict a new entity type in online comments. You'll write your own training loop from scratch, and understand the basics of how training works, along with tips and tricks that can make your custom NLP projects more successful.
This course uses spaCy v2. An updated version for the new spaCy v3 is coming soon. Luckily, the usage and API hasn't changed much, so everything you'll learn in this course is still relevant. See what's new in v3 →

Let’s write a simple training loop from scratch!

The pipeline you’ve created in the previous exercise is available as the nlp object. It already contains the entity recognizer with the added label "GADGET".

The small set of labelled examples that you’ve created previously is available as TRAINING_DATA. To see the examples, you can print them in your script.

    Call nlp.begin_training, create a training loop for 10 iterations and shuffle the training data.
    Create batches of training data using spacy.util.minibatch and iterate over the batches.
    Convert the (text, annotations) tuples in the batch to lists of texts and annotations.
    For each batch, use nlp.update to update the model with the texts and annotations.
****************************************************************************************'''
import spacy
import random
import json

​TRAINING_DATA = [['How to preorder the o.s.-21b', {'entities': [[20, 28, 'GADGET']]}],
                 ['o.s.-21b is coming', {'entities': [[0, 8, 'GADGET']]}],
                 ['Should I pay $1,000 for the op.sp.21?',
                            {'entities': [[28, 36, 'GADGET']]}],
                 ['The O.Spe.21 reviews are here', {'entities': [[4, 12, 'GADGET']]}],
                 ['Your os-21b goes up to 11 today', {'entities': [[5, 11, 'GADGET']]}],
                 ['I need a new phone! Any tips?', {'entities': []}]]
print(TRAINING_DATA)
​
nlp = spacy.blank("en")
ner = nlp.create_pipe("ner")
nlp.add_pipe(ner)
ner.add_label("GADGET")

​# Start the training
nlp.begin_training()

​# Loop for 10 iterations
for itn in range(10):
    # Shuffle the training data
    random.shuffle(TRAINING_DATA)
    losses = {}

    # Batch the examples and iterate over them
    for batch in spacy.util.minibatch(TRAINING_DATA, size=2):
        texts = [text for text, entities in batch]
        annotations = [entities for text, entities in batch]

​        # Update the model
        nlp.update(texts, annotations, losses=losses)
    print(losses)


text="Nella terza e nella quarta colonna, l’unità di misura ed il quantitativo preventivato per\nciascuna voce..\n\nIl suddetto Modulo dovrà essere o.s.-21b nella quinta colonna (in cifre) e nella sesta\ncolonna (in lettere) con i prezzi unitari che i partecipanti si dichiarano disposti ad offrire per\nogni voce relativa alle varie categorie di lavoro e os-21b e, nella settima colonna (in cifre).Nella terza e nella o.s.-21 colonna, l’unità di misura ed il quantitativo preventivato per\nciascuna voce..\n\nIl suddetto Modulo dovrà essere completato nella quinta colonna (in cifre) e nella sesta\ncolonna (in lettere) con i prezzi unitari che i partecipanti si dichiarano disposti ad offrire per\nogni voce relativa alle varie categorie di lavoro e fornitura e, nella settima colonna (in cifre).Nella terza e nella quarta colonna, l’unità di misura ed il quantitativo preventivato per\nciascuna voce..\n\nIl suddetto Modulo dovrà essere completato nella quinta os-21b (in cifre) e nella os-21B\ncolonna (in lettere) con i prezzi unitari che i partecipanti si dichiarano disposti ad offrire per\nogni voce relativa alle varie categorie di lavoro e fornitura e, nella settima colonna (in cifre)"
# Process the text
doc = nlp(text)

# Iterate over the entities
for ent in doc.ents:
    # Print the entity text and label
    print(ent.text, ent.label_)


'''**************************************
[['How to preorder the o.s.-21b', {'entities': [[20, 28, 'GADGET']]}], ['o.s.-21b is coming', {'entities': [[0, 8, 'GADGET']]}], ['Should I pay $1,000 for the op.sp.21?', {'entities': [[28, 36, 'GADGET']]}], ['The O.Spe.21 reviews are here', {'entities': [[4, 12, 'GADGET']]}], ['Your os-21b goes up to 11 today', {'entities': [[5, 11, 'GADGET']]}], ['I need a new phone! Any tips?', {'entities': []}]]
{'ner': 30.36202049255371}
{'ner': 19.03453493118286}
{'ner': 8.54869403410703}
{'ner': 7.132327612838708}
{'ner': 3.4405767540447414}
{'ner': 0.9578352008247748}
{'ner': 0.23587325110202073}
{'ner': 0.016894001492502753}
{'ner': 6.293470630042153e-05}
{'ner': 9.936782742469305e-07}

About this course

spaCy is a modern Python library for industrial-strength Natural Language Processing. In this free and interactive online course, you'll learn how to use spaCy to build advanced natural language understanding systems, using both rule-based and machine learning approaches.
About me

I'm Ines, one of the core developers of spaCy and the co-founder of Explosion. I specialize in modern developer tools for AI, Machine Learning and NLP. I also really love building stuff for the web.

    spaCy WebsiteSourceFollow me on Twitter

Navigated to '''