from bs4 import BeautifulSoup
import requests
import re
import string
import numpy as np

glossary = []

# FIRST SOURCE OF WORDS: https://www.health.harvard.edu/medical-dictionary-of-health-terms

"""
This site stores vocabularies in the dictionary in
four different ranges: from a-c, d-i, j-p, and q-z
"""

# words ranges
words_intervals = ('ac', 'di', 'jp', 'qz')

# url template (of the dictionary)
url_template = 'https://www.health.harvard.edu/medical-dictionary-of-health-terms/{start}-through-{end}'

# store vacabularies
# vocabulary_harvard = []
vocabulary_harvard = {}

# loop over each range (each part of the dictionary)
for interval in words_intervals:
    # url of the current range
    url = url_template.format(start=interval[0], end=interval[1])
    # read/parse the web page (html/xml document)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    # extract the tags containing the vacabularies and their definitions
    text_data = soup.find('div', class_='e-content entry-content').text
    # loop over each line (text in each tag) to extract the vocab
    for line in text_data.split("\n"):
        # line from which there is no vacabulary anymore (end web page)
        if "Share this page:" in line:
            break
        # lines before the first vocabulary get removed and the vacabularies get extracted from each line (tag)
        if (':' in line) and (not line.startswith("Browse dictionary by letter")) and (not line.startswith('Published')):
            # vocabulary_harvard.append(line.split(':')[0])
            tagvalue = line.split(':')
            #print(tagvalue)
            vocabulary_harvard[tagvalue[0].strip()] = tagvalue[1].strip()

glossary += list(vocabulary_harvard.keys())


# unique set of the vacabs
# vocabulary_harvard = set([word.lower() for word in vocabulary_harvard])



# SECOND SOURCE OF WORDS: https://www.medicinenet.com

# url template (of the dictionary)
url_template = "https://www.medicinenet.com/script/main/alphaidx.asp?p={0}_dict"

# store vacabularies
wordsFrom_medicinenet = []

# loop over vacabularies starting with a, b, c, etc.
for letter in string.ascii_lowercase:
    # url of the current range
    url = url_template.format(letter)
    # read/parse the web page (html/xml document)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    # extract the tags containing the vacabularies (tags here contain vocabs with no definition)
    text_data = soup.find('div', class_='AZ_results').find_all('li')
    # extract the words from the tags
    for tag in text_data:
        wordsFrom_medicinenet.append(tag.text)

wordsFrom_medicinenet = [word.lower() for word in wordsFrom_medicinenet]

glossary += wordsFrom_medicinenet

# THIRD SOURCE: VACAB BY MEDICAL SUBFIELD

words_subfields = {}

# 1- Glossary of Immunological Terms: https://www.immunopaedia.org.za/glossary/
url = "http://www.repro-med.net/glossary-of-immunological-terms"
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
text_data = soup.find('div', class_='entry-content clearfix').find_all('strong')
words_subfields['immunology'] = [re.sub("\.$", "", tag.text).strip() for tag in text_data if len(tag.text) > 1]

# 2- dermatology
url = "https://courses.washington.edu/hubio567/lang/term2.html#:~:text=%20Dermatology%20Terminology%20%201%20Acne%20Vulgaris%20.,%2017%20Wheal%2C%20Welt%20.%20%20More%20"
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
words_subfields['dermatology'] = [tag.text.strip() for tag in soup.find_all('strong') if len(tag.text) > 1]

# 3- radiology
url = "https://www.radiologyinfo.org/en/glossary/browse-glossary.cfm?all=1"
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
text_data = soup.find('div', id='main-inner').find_all('strong')
words_subfields['radiology'] = [tag.text.strip() for tag in text_data if '\n' not in tag.text]

# 3- genetics
url = "https://en.wikipedia.org/wiki/Glossary_of_genetics"
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
text_data = soup.find_all('dfn', class_='glossary')
words_subfields['genetics'] = [tag.text.strip() for tag in text_data if not re.match('^(\d|[A-Z]-(DNA|value))', tag.text)]

# 4- neurology
url = "http://www.strokecenter.org/professionals/resources/glossary-of-neurological-terms/"
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
text_data = soup.find('ul', id='myList').find_all('strong')
words_subfields['neurology'] = [re.sub('(\n|\t)', '', x.text).strip() for x in soup.find('ul', id='myList').find_all('strong')]

glossary += list(words_subfields.keys())


# VOCABULARY FOR HEATHCARE
# source 1
health_care_words = []
url = 'https://www.theguardian.com/healthcare-network/2011/aug/22/glossary-nhs-healthcare-jargon-acronyms'
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
text_data = soup.find('div', class_="article-body-commercial-selector css-79elbk").find_all('strong')
health_care_words = set([tag.text.strip() for tag in text_data][1:-1])

glossary += health_care_words

# source 2
url = 'https://www.disabled-world.com/definitions/acronyms.php'
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
text_data = soup.find('table', class_="lists").find_all('td')
health_care_words = health_care_words.union([x.text.strip().lower() for x in text_data[1:]][::2])

glossary = sorted(list(health_care_words)) + glossary

#
url = 'https://www.thoughtco.com/important-healthcare-vocabulary-4018191'
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
text_data = soup.find_all('ul', class_="comp mntl-sc-block mntl-sc-block-html")
text_data = [y.text for el in text_data for y in el.find_all('li')]
words = [line.split('-')[0].strip() for line in text_data]

# from here, the code should be run line by line (not the whole file)
glossary = words + glossary
glossary = np.unique(glossary)

# export the vocabs
file_vocab = open('01-cris_MedicalWords_v01.txt', 'w')
file_vocab.writelines('\n'.join(glossary))
file_vocab.close()

#--------------------------------------------------------------------#

simplified_glossary = [x for x in glossary if (len(x)>=5) and re.match('^[A-Za-z][a-z0-9]+$', x)]
print(len(simplified_glossary))

file = open('cris_MedicalWords_v02_from_v01.txt', 'w')
file.writelines('\n'.join(simplified_glossary))
file.close()

#---------------------------------------------------------------------------#
