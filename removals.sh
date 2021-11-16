#!/bin/bash

rm 3.ner_spacy/output/ -r
rm 1.ner_regex/log 
rm 2.dataset_splitter/log 2.dataset_splitter/*.spacy
rm 3.ner_spacy/config.cfg 3.ner_spacy/*.spacy  3.ner_spacy/spacy_ner.json1
rm 4.scorer/regex.json1  4.scorer/scores_regex.json 4.scorer/scores_spacy.json 4.scorer/spacy.json1 
rm 5.json_to_csv/regex.csv  5.json_to_csv/scores_regex.json  5.json_to_csv/scores_spacy.json
