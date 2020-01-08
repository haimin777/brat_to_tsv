# BRAT to TSV dataset converter
This is a simple GUI-based Widget based on matplotlib in Python to facilitate quick and efficient crowd-sourced generation of annotation masks and bounding boxes using a simple interactive User Interface. Annotation can be in terms of polygon points covering all parts of an object (see instructions in README) or it can simply be a bounding box, for which you click and drag the mouse button. Optionally, one could choose to use a pretrained Mask RCNN model to come up with initial segmentations. This shifts the work load from painstakingly annotating all the objects in every image to altering wrong predictions made by the system which maybe simpler once an efficient model is learnt.

#### Note: First part of converter create dataset for only Relation extraction purpose with one tipe of relation. 

### REQUIREMENTS:

`Python 3.5+` and `pandas` have to be used .

#### RUNNING CONVERTER:

run in folder with cloned repository. `data` - path to directory with .ann and .txt files'
```
python converter.py -i data
```

