#########################################
# Done:
#   - Convert upper-case to lower-case
#   - Remove punctuation and special characters
#   - Remove numbers
#   - Remove stop words. A set of stop words is provided in the file “stop_words.txt”
#   - Tokenize paragraphs
#   - Perform stemming. Use the Porter stemming code provided in the file “Porter_Stemmer_X.txt”
#   - Extract most frequent words.
# To Do:
#   - Combine stemmed words. ?????????
#   - Cluster to group similar paragraphs together

import re
from PorterStemmer import PorterStemmer 

tokens = []
porter_stemmer = PorterStemmer()

def clean_text(input):
    input = input.lower() # remove capitalization
    # input = re.sub(r'\s+', ' ', input) # replace white space with a single space
    input = re.sub(r'[^\w\s]', '', input) # remove everything except words, space, and digits
    # ^ not sure if we want to remove hypens since it messes up some words
        # i.e. see American-Canadian in first paragraph (not sure if americancanadian should be treated
        #       as one token [prob should])
    input = re.sub(r'\d+', '', input) # remove all digits
    return input

def remove_stop_words(paragraph, stop_words):
    words = paragraph.split()
    tokens = []
    for word in words:
        if word not in stop_words:
            tokens.append(word)
    return tokens

def stem_tokens(tokens):
    i = 0
    stemmed_tokens = {}
    for paragraph in tokens:
        paragraph_index = i
        temp = []
        for token in paragraph:
            # print(porter_stemmer.stem(token, 0, len(token)- 1))
            stemmed_token = porter_stemmer.stem(token, 0, len(token)- 1)
            temp.append(stemmed_token)
        stemmed_tokens[paragraph_index] = temp
        i += 1
    return stemmed_tokens

def create_feature_vector(stemmed_tokens):
    feature_vector = {}
    i = 0
    for paragraph in stemmed_tokens:
        for token in stemmed_tokens[paragraph]:
            if token not in feature_vector:
                feature_vector[token] = i
                i += 1
    return feature_vector, i

def create_tdm(stemmed_tokens, feature_vector, dimensionality):
    tdm = []
    for paragraph in stemmed_tokens:
        feature_freq = [0 for _ in range(dimensionality)]
        for token in stemmed_tokens[paragraph]:
            feature_freq[feature_vector[token]] += 1
        tdm.append(feature_freq)
    return tdm

# read in text files and create objects
paragraphs_file = open("./paragraphs.txt", "r")
stop_words_file = open("./stop_words.txt", "r")
paragraphs_text = paragraphs_file.read()
stop_words = stop_words_file.read().split()


corpus = clean_text(paragraphs_text)
paragraphs = corpus.splitlines() # get each paragraph
for paragraph in paragraphs:
    if paragraph: # if it's not whitespace
        tokens.append(remove_stop_words(paragraph, stop_words)) # get tokens list for each paragraph

# for i, token in enumerate(tokens):
#     print("--------------------------------------------- " + str(i) + " --------------------------------------------- ")
#     print(token)
#     print(" ")

stemmed_tokens = stem_tokens(tokens)
feature_vector, dimensionality = create_feature_vector(stemmed_tokens)

tdm = create_tdm(stemmed_tokens, feature_vector, dimensionality)
print(tdm)

