
# PURPOSE: This file is used to clean all the words from the files
#          01-cris_MedicalWords_v01.txt,  01-john_MedicalWords_v01.txt,
#          01-enam_MedicalWords_v01.txt,  01-mamuzou_MedicalWords_v01.txt
#          which contains the 'unclean' medical words
# - A word is defined as clean if it contains only alphabet characters, is not an acronym
#   (not even partially), and is made up of at least 5 characters.
# - A word is defined as an acronym if it contains only capital letters or if some characters
#   after the first one are capital letters (example: HbA1c = hemoglobin A1c)


# import library
import re


# function to clean and save the words
def cleanWords(readfile: str, writefile: str) -> None:
    """
    function to clean and save the words
    
    :param readfile: path to the file containing the 'unclean' words
    :param writefile: path file to save the clean words
    :return: None
    """

    # read file containing the words
    file = open(readfile, "r")

    # remove the comma at the end of some words in the file
    words = [re.sub(",\n", "\n", line) for line in file]
    file.close()

    # clean the words
    words = [line.lower() for line in words if re.match('^[A-Za-z][a-z]+\n$', line) and (len(line)>5)]

    # save the words (to a different file)
    cleanWords = open(file=writefile, mode="w")
    cleanWords.writelines(''.join(words))
    cleanWords.close()


# clean and save the words
cleanWords(readfile='01-cris_MedicalWords_v01.txt', writefile='01-cris_MedicalWordsClean_v01.txt')
cleanWords(readfile='01-john_MedicalWords_v01.txt', writefile='01-john_MedicalWordsClean_v01.txt')
cleanWords(readfile='01-mamuzou_MedicalWords_v01.txt', writefile='01-mamuzou_MedicalWordsClean_v01.txt')
cleanWords(readfile='01-enam_MedicalWords_v01.txt', writefile='01-enam_MedicalWordsClean_v01.txt')
 

# save all words in one file
files = ['01-cris_medicalWordsClean_v01.txt', '01-john_MedicalWordsClean_v01.txt',
         '01-mamuzou_MedicalWordsClean_v01.txt', '01-enam_MedicalWordsClean_v01.txt']

## list to store all the words
allWords = []

for file in files:
    # read corrent file
    fileWords = open(file=file, mode="r")
    
    # add to the list of all words
    allWords += [line for line in fileWords]
    fileWords.close()

## 
allWordsFile = open(file='01-allMedicalWords_v01.txt', mode="w")

## list of all words in alphabetic order (unique set of words)
allWordsFile.writelines(''.join(sorted(list(set(allWords)))))
allWordsFile.close()


