#!/bin/sh

spacy init fill-config base_config.cfg config.cfg
spacy train config.cfg --paths.train ./train.spacy --paths.dev ./dev.spacy --output ./output

