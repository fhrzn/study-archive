import string
import torch

# constant
ALL_LETTERS = string.ascii_letters + '.,;'
N_LETTERS = len(ALL_LETTERS)
EPOCH = 100
LEARNING_RATE = 0.001
TEST_SIZE = 0.2
VAL_SIZE = 0.2
DATA_PATH = './data/names/'
DEVICE = torch.device('cuda' if torch.cuda.is_available else 'cpu')
PRINT_EVERY = 10
LOG_EVERY = 1000    # we can consider it as batch size
LOG_LEVEL='PROD'
MODEL_NAME = 'model.pt'
EARLY_STOP = 5