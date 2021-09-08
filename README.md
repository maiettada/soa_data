# soa_data

**Modules**: 
1. Regex information extraction: python script that extracts soa data with the usage of regular expressions;
2. scorer for regex-extracted data: takes in input some regex-extracted soa data (v1, v2 or v3, retrieved by using different regex) and scores them by comparing them to the ground truth;
3. dataset train dev test production: takes a gold.json1 file describing the ground truth; divides it into many labelled sentences, distributing them to the train/dev/test bins;
It's a necessary step for the setup of a NER task in spacy;
4. json to csv: helper script to convert Spacy-scores from json format to csv format. 
