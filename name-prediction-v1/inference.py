import torch
from network import NameRNN
from constant import N_LETTERS, DATA_PATH, DEVICE
from dataloader import load_data
from dataprep import one_hot_encode
from utils import output_to_label

def load_model(path):
    '''docstring'''
    checkpoint = torch.load(path)
    return checkpoint


def predict(model, name):
    print(f'>>> {name}')
    
    with torch.no_grad():
        encode_name = one_hot_encode(name)
        encode_name = encode_name.to(DEVICE)
        # print(encode_name)

        # init hidden state
        hidden = model.init_hidden(DEVICE)
        # print(hidden)

        for row in encode_name:
            # add dimension
            row = row.view(1, -1)
            # forward pass
            output, hidden = model(row, hidden)

    return output


if __name__ == '__main__':

    # load checkpoint
    print('Load model checkpoint...')
    path = './model.pt'
    checkpoint = load_model(path)

    # get labels
    print('Load labels...')
    _, labels = load_data(DATA_PATH)
    n_categories = len(labels)

    # define network and apply loaded checkpoint
    print('Apply checkpoints to model...')
    hidden_size = 128
    model = NameRNN(N_LETTERS, hidden_size, n_categories)
    model.load_state_dict(checkpoint)
    model.to(DEVICE)

    # put to eval mode
    model.eval()

    print('\n')

    # prompt user to input
    while True:
        name = input('Input name: ')
        if name == 'quit':
            break
    
        output = predict(model, name)
        _, predicted = output_to_label(labels, output)
        print(f'Predicted Country: {predicted}', end='\n\n')