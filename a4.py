#########################################
# Done:
#   - Convert upper-case to lower-case
#   - Remove punctuation and special characters
#   - Remove numbers
#   - Remove stop words. A set of stop words is provided in the file “stop_words.txt”
#   - Tokenize paragraphs
# To Do:
#   - Perform stemming. Use the Porter stemming code provided in the file “Porter_Stemmer_X.txt”
#   - Combine stemmed words.
#   - Extract most frequent words.

import re

tokens = []

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

for i, token in enumerate(tokens):
    print("--------------------------------------------- " + str(i) + " --------------------------------------------- ")
    print(token)
    print(" ")

