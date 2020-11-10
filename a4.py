import re
from PorterStemmer import PorterStemmer 
import operator
import math
import numpy as np
import pandas as pd

tokens = []
porter_stemmer = PorterStemmer()
alpha = 1

def clean_text(input):
    input = input.lower() # remove capitalization
    # input = re.sub(r'\s+', ' ', input) # replace white space with a single space
    input = re.sub(r'[^\w\s]', '', input) # remove everything except words, space, and digits
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
    doc_freqs = {}
    tfidf = {}
    total_word_count = 0

    # get word freqs
    for paragraph in stemmed_tokens:
        for token in stemmed_tokens[paragraph]:
            total_word_count += 1
            if token not in doc_freqs:
                doc_freqs[token] = {}
                doc_freqs[token][paragraph] = 1
            elif paragraph not in doc_freqs[token]:
                doc_freqs[token][paragraph] = 1

            if token not in word_freqs:
                word_freqs[token] = 1
            else:
                word_freqs[token] += 1

    for token in word_freqs:
        tfidf[token] = (word_freqs[token] / total_word_count) * (16 / len(doc_freqs[token].keys()))

    # sort frequencies in descending order
    sorted_freqs = dict(sorted(tfidf.items(), key=operator.itemgetter(1),reverse=True))
    most_freq_words = {}
    i = 0
    for word in sorted_freqs:
        if(i > (limit - 1)):
            break
        else:
            most_freq_words[word] = i
            i += 1
    print(most_freq_words)
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
    all_clusters.append((tdm[0], 0, [0])) # the cluster weights, m value, list of occupying nodes
    for i in range(1, len(tdm)):
        pattern = tdm[i]
        closest_cluster = None # index of the closest cluster
        closest_distance = None # the closest_distance of current pattern
        current_m = None
        for j in range(len(all_clusters)):
            current_cluster, m, nodes = all_clusters[j]
            ed = get_euclidean_distance(pattern, current_cluster)
            if (ed <= threshold):
                if closest_cluster is None:
                    closest_cluster = j
                    closest_distance = ed
                    current_m = m
                elif (ed < closest_distance):
                    closest_cluster = j
                    closest_distance = ed
                    current_m = m
        if closest_cluster is None:
            all_clusters.append((pattern, 0, [i]))
        else:
            m = current_m
            wk = ((m / (m + 1)) * all_clusters[closest_cluster][0]) + ((alpha / (m + 1)) * pattern)
            all_clusters[closest_cluster][2].append(i)
            all_clusters[closest_cluster] = (wk, m + 1,
                    all_clusters[closest_cluster][2])

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
feature_vector, dimensionality = create_feature_vector(stemmed_tokens, 9)

# make the tdm and print to a csv file
tdm = create_tdm(stemmed_tokens, feature_vector, dimensionality)
tdm_df = pd.DataFrame(tdm)
tdm_df.columns = feature_vector.keys()
tdm_df.index.name = 'paragraph'
tdm_df.to_csv('tdm.csv')

# make the clusters
clusters = cluster(tdm, 10, alpha)

for i in range(len(clusters)):
    current_cluster = clusters[i]
    print("")
    print("Info for cluster: ", i)
    print("Number of paragraphs in this cluster: ", len(current_cluster[2]))
    print("Paragraphs grouped together: ", current_cluster[2])
    print("Center of cluster: ", current_cluster[0])
    print("")

