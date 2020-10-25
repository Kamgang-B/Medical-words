# Medical-words

_Medical-words_ is a project for Python Lab subject.
The purpose of this project is to train a model that takes as input medical and healthcare words converted into images and predict them.
To each word, we will also associate its pronunciation (as a .wav or .mp3); in other words, each word will be matched to two files: an image file
containing the word and a .wav or .mp3 file containing its sound (how it is pronounced). The .wav or .mp3 files obtained will be used as input in another model 
different from _Medical-words_ project.


## Description of the different steps from data collection to image generation

* The words are downloaded from internet/web (using [01-cris_scrapedWords_v01.py](https://github.com/kaboc7/Medical-words/blob/main/src/data/01-cris_scrapedWords_v01.py), (others' scripts??) ) and store in [data/raw](https://github.com/kaboc7/Medical-words/tree/main/data/raw).    
* These words are then clean (using [02-cleanWords_v01.py](https://github.com/kaboc7/Medical-words/blob/main/src/data/02-cleanWords_v01.py) in [src/data](https://github.com/kaboc7/Medical-words/tree/main/src/data) ) which produces the files in [data/interim](https://github.com/kaboc7/Medical-words/tree/main/data/interim).    
* These files are pulled together to create a unique database for clean words (stored in [data/processed](https://github.com/kaboc7/Medical-words/tree/main/data/processed) ) as [01-allMedicalWords_v01](https://github.com/kaboc7/Medical-words/blob/main/data/processed/01-allMedicalWords_v01.txt).
*    These words are finally converted into images (using [03-convertWordsIntoImages_v01.py](https://github.com/kaboc7/Medical-words/blob/main/src/data/03-convertWordsIntoImages_v01.py) in [src/data](https://github.com/kaboc7/Medical-words/tree/main/src/data) 

The image below describes this process.

![Untitled Diagram2](https://user-images.githubusercontent.com/72712004/97102438-d3936800-16a5-11eb-88e6-c1f5e4ea7aa8.png)
