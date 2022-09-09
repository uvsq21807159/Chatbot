import json
import os
import numpy as np
import pickle
from normalizer import IGNORE_WORDS, bag_of_words, stem_and_lower, tokenize


with open("./src/chatbot/intents.json", "r") as file:
    intents = json.load(file)


def train_data(datafile):
    all_words = []
    tags = []
    words_tags = [] # each iteration corresponds to a pattern associated with its tag
    # loop through each sentence in our intents patterns
    for intent in intents["intents"]:
        tag = intent["tag"]
        tags.append(tag)
        for pattern in intent["patterns"]:
            words = tokenize(pattern)
            words = [stem_and_lower(word) for word in words if word not in IGNORE_WORDS]
            all_words.extend(words)
            # add the pattern_tag pair to the list
            words_tags.append((words, tag))

    # sort and remove duplicates (by using sort)
    all_words = sorted(list(set(all_words)))
    tags = sorted(tags)

    bags = []
    tags_i = []
    # create training data
    for (pattern_sentence, tag) in words_tags:
        bag = bag_of_words(pattern_sentence, all_words)
        bags.append(bag)
        tag_i = np.zeros(len(tags), dtype=np.int32)
        tag_i[tags.index(tag)] = 1
        tags_i.append(tag_i)

    bags = np.array(bags)
    tags_i = np.array(tags_i)

    os.makedirs(os.path.dirname(datafile), exist_ok=True)
    with open(datafile, 'wb') as file:
        pickle.dump((all_words, tags, bags, tags_i), file)

