#########################################
# Done:
#   - Convert upper-case to lower-case
#   - Remove punctuation and special characters
#   - Remove numbers
# To Do:
#   - Tokenize paragraphs
#   - Remove stop words. A set of stop words is provided in the file “stop_words.txt”
#   - Perform stemming. Use the Porter stemming code provided in the file “Porter_Stemmer_X.txt”
#   - Combine stemmed words.
#   - Extract most frequent words.

import re

def clean_text(input):
    input = input.lower() # remove capitalization
    # input = re.sub(r'\s+', ' ', input) # replace white space with a single space
    input = re.sub(r'[^\w\s]', '', input) # remove everything except words and space
    # ^ not sure if we want to remove hypens since it messes up some words
        # i.e. see American-Canadian in first paragraph (not sure if americancanadian should be treated
        #       as one token [prob should])
    input = re.sub("\d+", "", input) # remove all digits
    return input

paragraphs_file = open("./paragraphs.txt", "r")
paragraphs = paragraphs_file.read()
corpus = clean_text(paragraphs)
print(corpus)