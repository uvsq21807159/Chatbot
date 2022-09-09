import pickle
import tensorflow as tf
import tflearn as tfl
from train import train_data

#retrieve data from a file
def load_data(datafile):
    with open(datafile, "rb") as file:
        all_words, tags, bags, tags_i = pickle.load(file)
        return all_words, tags, bags, tags_i


def create_model(datafile):

    try:
        all_words, tags, bags, tags_i = load_data(datafile)
    except:
        train_data(datafile)
        all_words, tags, bags, tags_i = load_data(datafile)

    HIDDEN_NEURONS = int((len(all_words) + len(tags)) / 2)

    #creation of a neural network composed of 4 layers 
    net = tfl.input_data(shape=[None, len(all_words)])
    net = tfl.fully_connected(net, HIDDEN_NEURONS)
    net = tfl.fully_connected(net, HIDDEN_NEURONS)
    net = tfl.fully_connected(net, len(tags), activation="softmax")
    net = tfl.regression(net)

    #DNN is a type of neural network
    model = tfl.DNN(net)

    try:
        model.load("data/model.tflearn")
    except:
        model = tfl.DNN(net)
        model.fit(bags, tags_i, n_epoch=50, batch_size=4, show_metric=True)
        model.save("data/model.tflearn")

    return model, all_words, tags