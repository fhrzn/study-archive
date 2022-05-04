import torch

DATA_PATH = './data/names.txt'
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
PRINT_EVERY = 100
BATCH_SIZE = 64
EPOCH = 1000
LR = 0.0001  # Learning Rate
ES = 5      # Early Stop
TRAIN_SIZE = .8
TEST_SIZE = .2
VAL_SIZE = .5
GRAD_CLIP = 5
MODEL_PATH = './models/name_gen{}.pt'
HID_SIZE = 128
EMB_SIZE = 64
