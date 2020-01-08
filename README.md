# BRAT to TSV dataset converter
This is a simple comand line tool for converting dataset annotated in BRAT format to format that accept BERT style NN: `https://github.com/dmis-lab/biobert`
#### Note: First part of converter create dataset for only Relation extraction purpose with one tipe of relation. 

### REQUIREMENTS:

`Python 3.5+` and `pandas` have to be used .

#### RUNNING CONVERTER:

run in folder with cloned repository. `data` - path to directory with .ann and .txt files'
```
python converter.py -i data
```

