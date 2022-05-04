import numpy as np
import random
import torch
from torch.utils.data import TensorDataset, DataLoader
import pickle
from constant import BATCH_SIZE, DATA_PATH

def load_data(path):
    
    try:
        with open(path, 'r', encoding='utf-8') as r:
            names = r.read().split('\n')
    except:
        print('Path not found / not accessible. Please check path again.')
        return

    # shuffle dataset
    index = list(range(len(names)))
    random.shuffle(index)
    names = [names[i] for i in index]

    return names

def build_vocab(names):
    # get all possible chars
    chars = tuple(set(''.join(names)))

    # map int to char
    # start vocab index from 1, cz we'll put <PAD> token in index 0
    int2char = dict(enumerate(chars, 1))
    int2char[0] = '<PAD>'

    # map back char to int
    char2int = {v: k for k, v in int2char.items()}

    # save vocab to disk
    pickle.dump(char2int, open('./models/vocab.pkl', 'wb'))
    pickle.dump(int2char, open('./models/vocab_int2char.pkl', 'wb'))

    return char2int, int2char

def encode_words(names, vocab):    
    # encode words
    return [[vocab[ch] for ch in name] for name in names]

def pad_features(names, seq_length=None):
    # if seq_length is None, then select the longest feature as maximum
    if seq_length == None:
        seq_length = max([len(x) for x in names])

    # create seros-like array for feature template
    features = np.zeros((len(names), seq_length), dtype=int)

    # fill feature template from front
    for i, row in enumerate(names):
        features[i, :len(row)] = np.array(row)[:seq_length]

    # make sure total features and total names is equal
    assert len(features) == len(names)
    # make sure length features is equal with max sequence length
    assert len(features[0]) == seq_length

    return features

def split_data(x, train_size=.8, test_size=.2, val_set=True, val_size=.5):
    '''Split datasets into train, test, and validation set (optional).
    -------------------------
    Parameters:
    x           : Feature vector
    y           : Label
    train_size  : Train set fraction of all data (float)
    test_size   : Test set fraction of all data (float)
    val_set     : Generate validation set if True (bool)
    val_size    : Validation set fraction of test set. Default to 0.5, 
                  means divide test set into 2 equals part. (float)
    '''

    # make a train set
    train_id = int(len(x) * train_size)
    train_x, remain_x = x[:train_id], x[train_id:]

    # make a test set
    if val_set == False:
        # treat remain_x and remain_y as test set
        return (train_x, remain_x)

    else:
        val_id = int(len(remain_x) * val_size)
        val_x, test_x = remain_x[:val_id], remain_x[val_id:]

        return (train_x, test_x, val_x)

def make_batch(train_feature, test_feature, valid_feature=None, batch_size=64):
    '''Generate data batch using PyTorch Dataset and DataLoader.
    -------------------------
    Parameters:
    train_feature   : Train feature (tuple).
    test_feature    : Test feature (tuple).
    valid_feature   : Validation feature (tuple).
    batch_size      : Batch size. Default to 64 (int).
    '''

    # generate TensorDataset
    trainset = TensorDataset(torch.from_numpy(train_feature))
    testset = TensorDataset(torch.from_numpy(test_feature))

    # if validation feature provided
    if valid_feature != None:
        validset = TensorDataset(torch.from_numpy(valid_feature))

    # generate DataLoader
    trainloader = DataLoader(trainset, shuffle=True, batch_size=batch_size)
    testloader = DataLoader(testset, shuffle=True, batch_size=batch_size)

    try:
        valloader = DataLoader(validset, shuffle=True, batch_size=batch_size)

        return trainloader, testloader, valloader

    except:
        # validation feature were not provided.
        return trainloader, testloader

def load(path):
    # load dataset
    names = load_data(path)

    try:
        # load vocab
        vocab = pickle.load(open('./models/vocab.pkl', 'rb'))
        int2char = pickle.load(open('./models/vocab_int2char.pkl', 'rb'))
        print('Use existing vocabulary.')
    except:
        # build vocab
        vocab, int2char = build_vocab(names)

    # encode words
    enc_words = encode_words(names, vocab)
    # pad features
    padded = pad_features(enc_words)
    # split data
    train, test = split_data(padded, val_set=False)
    # make batch
    trainloader, testloader = make_batch(train, test, batch_size=BATCH_SIZE)

    return (trainloader, testloader), vocab, int2char

if __name__ == '__main__':

    # load dataset
    loader, vocab = load(DATA_PATH)
    trainloader, testloader = loader
    print(len(vocab))
    print(len(trainloader))
    print(len(testloader))