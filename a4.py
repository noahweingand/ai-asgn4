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
import operator
import math
import numpy as np

tokens = []
porter_stemmer = PorterStemmer()
alpha = 1

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

def create_feature_vector(stemmed_tokens, limit):
    word_freqs = {}
    for paragraph in stemmed_tokens:
        for token in stemmed_tokens[paragraph]:
            if token not in word_freqs:
                word_freqs[token] = 1
            else:
                word_freqs[token] += 1
    # sort frequencies in descending order
    sorted_freqs = dict(sorted(word_freqs.items(), key=operator.itemgetter(1),reverse=True))
    most_freq_words = {}
    i = 0
    for word in sorted_freqs:
        if(i > (limit - 1)):
            break
        else:
            most_freq_words[word] = i
            i += 1
    #print(most_freq_words)
    return most_freq_words, i

def create_tdm(stemmed_tokens, feature_vector, dimensionality):
    tdm = []
    for paragraph in stemmed_tokens:
        feature_freq = [0 for _ in range(dimensionality)]
        for token in stemmed_tokens[paragraph]:
            if token in feature_vector:
                feature_freq[feature_vector[token]] += 1
        tdm.append(feature_freq)
    return np.array(tdm)


def get_euclidean_distance(pattern, cluster_weights):
    operand = 0
    for i in range(len(pattern)):
        x1 = pattern[i]
        x2 = cluster_weights[i]
        operand += (x1 - x2)**2
    return math.sqrt(operand)


# FCAN clustering
def cluster(tdm, threshold, alpha):
    # wk = (m * wk + alpha * X) / (m + 1)
    all_clusters = []
    all_clusters.append((tdm[0], 0))
    for i in range(1, len(tdm)):
        pattern = tdm[i]
        closest_cluster = None
        current_m = None
        for j in range(len(all_clusters)):
            current_cluster, m = all_clusters[j]
            ed = get_euclidean_distance(pattern, current_cluster)
            if (ed <= threshold):
                if closest_cluster is None:
                    closest_cluster = j
                    current_m = m
                elif (ed < closest_cluster):
                    closest_cluster = j
                    current_m = m
        if closest_cluster is None:
            all_clusters.append((pattern, 0))
        else:
            m = current_m
            wk = ((m / (m + 1)) * closest_cluster) + ((alpha / (m + 1)) * pattern)
            all_clusters[j] = (wk, m + 1)
    return all_clusters

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
feature_vector, dimensionality = create_feature_vector(stemmed_tokens, 20)


tdm = create_tdm(stemmed_tokens, feature_vector, dimensionality)
#print(tdm)
clusters = cluster(tdm, 15, alpha)
print(len(clusters))

