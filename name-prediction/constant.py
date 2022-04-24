import torch

DATA_PATH = './data/'
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
PRINT_EVERY = 10
BATCH_SIZE = 64
EPOCH = 100
LR = 0.0001  # Learning Rate
ES = 5      # Early Stop
TRAIN_SIZE = .8
TEST_SIZE = .2
VAL_SIZE = .5
GRAD_CLIP = 5
MODEL_PATH = './models/name_rnn{}.pt'
HID_SIZE = 128
EMB_SIZE = 64
