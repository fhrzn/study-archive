from network import NameRNN
from dataloader import load_data, split
import torch
from torch.optim import Adam
from constant import EPOCH, LEARNING_RATE, N_LETTERS, PRINT_EVERY, TEST_SIZE, VAL_SIZE, DATA_PATH, DEVICE, LOG_EVERY
from train import training
import time


if __name__ == '__main__':
    # load our dataset
    print('Loading data...')
    data, labels = load_data(DATA_PATH)
    n_categories = len(labels)

    # split our dataset into train and test
    print('Split into train - test')
    train, test = split(data, TEST_SIZE)
    # unpack train zip
    # feature, label = zip(*train)
    # split our train set into train and val
    print('Split into train - val')
    train, val = split(train, VAL_SIZE)    
    

    print('Initializing model...')
    # define hidden size
    hidden_size = 128
    # model initialization
    network = NameRNN(N_LETTERS, hidden_size, n_categories)    
    
    # train
    print('Training start...')
    start = time.time()
    result = training(network, labels, train, val, DEVICE, EPOCH, LEARNING_RATE, PRINT_EVERY, LOG_EVERY)
    print(f'Training done. Time elapsed {time.time() - start:.2f} second')
    