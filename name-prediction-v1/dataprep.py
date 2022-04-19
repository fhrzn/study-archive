import torch
from constant import ALL_LETTERS


def one_hot_encode(letter):
    '''docstring'''

    def _get_char_position(char):
        return ALL_LETTERS.index(char)
    
    # initiate zero matrix
    onehot = torch.zeros((len(letter), len(ALL_LETTERS)), dtype=torch.float32)
    # fill corresponding position with 1
    for i, char in enumerate(letter):
        onehot[i][_get_char_position(char)] = 1

    return onehot


def encodes(arr):
    return [one_hot_encode(i) for i in arr]


if __name__ == '__main__':
    # one-hot encode test
    # print(one_hot_encode('Nasonov'))
    print(encodes(['Ria', 'Ari']))