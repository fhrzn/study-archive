import numpy as np
import os
import random
from torch.utils.data import TensorDataset, DataLoader
import torch
from constant import BATCH_SIZE
import pickle

def load_data(path):
    names, labels = [], []
    all_labels = []

    for f in os.listdir(path):
        label = f[:-4]
        all_labels.append(label)

        with open(path + f, encoding='utf-8') as r:
            lines = r.read().strip().split('\n')

            names.extend(lines)
            labels.extend([label for _ in range(len(lines))])

    # make sure each name paired with a label
    assert len(names) == len(labels)

    # shuffle dataset
    index = list(range(len(names)))
    random.shuffle(index)
    names = [names[i] for i in index]
    labels = [labels[i] for i in index]

    # save labels to disk
    pickle.dump(all_labels, open('./models/labels.pkl', 'wb'))

    return names, labels, all_labels

def build_vocab(names):
    # get all possible chars
    chars = tuple(set(''.join(names)))
    
    # map int to char
    # start vocab index from 1, bcs we'll put <PAD> char in index 0
    int2char = dict(enumerate(chars, 1))
    int2char[0] = '<PAD>'

    # map back char to int
    char2int = {v: k for k, v in int2char.items()}

    # save vocab to disk
    pickle.dump(char2int, open('./models/vocab.pkl', 'wb'))

    return char2int

def encode_words(names, vocab):
    return [[vocab[ch] for ch in name] for name in names]

def encode_labels(labels, labeldict):
    return np.array([labeldict.index(x) for x in labels])

def pad_features(names, seq_length=None):
    # if seq_length is None, then select the longest feature as maximum
    if seq_length == None:
        seq_length = max([len(x) for x in names])


    # create zeros-like array for feature template
    features = np.zeros((len(names), seq_length), dtype=int)    

    # fill feature template from back
    for i, row in enumerate(names):                           
        features[i, -len(row):] = np.array(row)[:seq_length]

    # make sure total features and total names is equal
    assert len(features) == len(names)
    # make sure length features is equal with max sequence length
    assert len(features[0]) == seq_length

    return features

def split_data(x, y, train_size=.8, test_size=.2, val_set=True, val_size=.5):
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
    train_y, remain_y = y[:train_id], y[train_id:]

    # make a test set
    if val_set == False:
        # treat remain_x and remain_y as test set
        return (train_x, train_y), (remain_x, remain_y)

    else:
        val_id = int(len(remain_x) * val_size)
        val_x, test_x = remain_x[:val_id], remain_x[val_id:]
        val_y, test_y = remain_y[:val_id], remain_y[val_id:]

        return (train_x, train_y), (test_x, test_y), (val_x, val_y)

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
    trainset = TensorDataset(
                            torch.from_numpy(train_feature[0]),
                            torch.from_numpy(train_feature[1]))
    testset = TensorDataset(
                            torch.from_numpy(test_feature[0]),
                            torch.from_numpy(test_feature[1]))
    
    # if validation feature provided
    if valid_feature != None:
        validset = TensorDataset(
                                torch.from_numpy(valid_feature[0]),
                                torch.from_numpy(valid_feature[1]))

    # generate DataLoader
    train_loader = DataLoader(trainset, shuffle=True, batch_size=batch_size)
    test_loader = DataLoader(testset, shuffle=True, batch_size=batch_size)

    try:
        val_loader = DataLoader(validset, shuffle=True, batch_size=batch_size)
        
        return train_loader, test_loader, val_loader

    except:
        # validation feature were not provided.
        return train_loader, test_loader

def load(path):
    # load dataset
    names, labels, all_labels = load_data(path)    
    try:
        # load vocab
        vocab = pickle.load(open('./models/vocab.pkl', 'rb'))
        print('Use existing vocabulary.')
    except:
        # build vocab
        vocab = build_vocab(names)
                
    # encode words
    enc_words = encode_words(names, vocab)
    # encode labels
    enc_labels = encode_labels(labels, all_labels)
    # pad features
    padded = pad_features(enc_words)
    # split data
    train, test, val = split_data(padded, enc_labels, train_size=.8)
    # make batch
    train_loader, test_loader, val_loader = make_batch(train, test, val, batch_size=BATCH_SIZE)

    return (train_loader, test_loader, val_loader), vocab, all_labels

if __name__ == '__main__':
    
    # load dataset
    path = './data/'

    # load
    loader, vocab, labels = load(path)
    train_loader, test_loader, val_loader = loader
    print(len(vocab))
    print(len(train_loader))
    print(len(test_loader))
    print(len(val_loader))