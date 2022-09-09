import numpy as np
import nltk

nltk.download("punkt")
from nltk.stem.porter import PorterStemmer

IGNORE_WORDS = ["?", ".", "!", ",", ";", "..."]
stemmer = PorterStemmer()


def tokenize(sentence):
    """
    Takes as parameter a string corresponding to a sentence and returns a list of words,
    numbers and other punctuation characters of this sentence.
    """
    return nltk.word_tokenize(sentence)


def stem_and_lower(word):
    """
    Returns the root of a word and lower all his letters.
    This allows to gather words that have the same root.
    For example : ['Pollution', 'Polluer', 'Polluante']
    -> ['pollut', 'polluer', 'polluant']
    """
    return stemmer.stem(word.lower())


def bag_of_words(stemmed_sentence, words):
    """
    Returns a vector of occurrences of a phrase separated into tokens compared to a list of
    single words. 1 for each known word that exists in the sentence, 0 otherwise
    example (without stemming):
    sentence = ["quelle", "est", "la", "pollution", "en", "france"]
    words = ["pollution", "qualité", "france", "air", "dangereux", "bonjour", "merci", "salut"]
    > [1, 0, 1, 0, 0, 0, 0, 0]
    """
    # initializing bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.int32)
    for i, word in enumerate(words):
        if word in stemmed_sentence:
            bag[i] = 1
    return bag


""" 
print("words_length : " + str(len(all_words)) + "\ntags_length : " + str(len(tags)))
wait(1)
"""
