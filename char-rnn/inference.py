import torch
from torch.nn import functional as F
from dataloader import encode_words, pad_features
import pickle
import numpy as np
from constant import DEVICE, HID_SIZE, EMB_SIZE, MODEL_PATH
from network import RNNNameGenerator, LSTMNameGenerator, GRUNameGenerator

def load_model(path):
    checkpoint = torch.load(path)
    return checkpoint

def generate(model, vocab, start_phrase='A', max_length=6, temperature=1.0, top_k=None):

    with torch.no_grad():
        #  encode start phrase
        x_enc = [[vocab[ch] for ch in start_phrase]]
        
        # here we dont need to pad the vector
        # convert encoded phrase to tensor
        x_torch = torch.tensor(x_enc, dtype=torch.int64)

        # create list for output
        char_out = start_phrase.split()

        # move to device
        x_torch = x_torch.to(DEVICE)
        model = model.to(DEVICE)

        # init empty hidden state
        h = None

        # running through start phrase to generate hidden_state
        # here we leave the last character cz we will feed it in
        # the generating phase as the first sequence
        for i in range(len(start_phrase)-1):
            out, h = model(x_torch[:, i:i+1], h)

        # start generating
        for _ in range(max_length - len(start_phrase)):
            out, h = model(x_torch[:, -1:], h)
            p = F.softmax(out / temperature, dim=-1).data

            # pick top K token by top_k (if defined)
            if top_k is None:
                top_char = np.arange(len(vocab))
            else:
                p, top_char = p.topk(top_k)
                top_char = top_char.cpu().numpy().squeeze()

            # select next token and push it to input sequence
            p = p.cpu().numpy().squeeze()
            char_id = np.random.choice(top_char, p=p/p.sum())
            char = torch.tensor([[char_id]], dtype=torch.int64)
            
            # make sure generated char in the same device
            char = char.to(DEVICE)
            # concat with current input sequence
            x_torch = torch.cat([x_torch, char], dim=-1)

            # push to char_out
            char_out.append(model.int2char[char_id] if char_id > 0 else '')

        return ''.join(char_out)

if __name__ == '__main__':

    # load vocabs
    print('Load vocabs...')
    vocab = pickle.load(open('./models/vocab.pkl', 'rb'))
    int2char = pickle.load(open('./models/vocab_int2char.pkl', 'rb'))

    # load model
    print('Load model checkpoint')
    path = './models/name_genLSTM.pt'
    model_weights = load_model(path)

    # define network
    print('Apply checkpoints to model...')
    model = LSTMNameGenerator(len(vocab), HID_SIZE, EMB_SIZE, char2int=vocab, int2char=int2char)
    model.load_state_dict(model_weights)

    # put model to eval mode
    model.eval()

    print('\n')

    # prompt user to input start phrase
    mlength = int(input('Max name characters: '))
    total_gen = int(input('How many names do you want to generate: '))
    while True:
        first_char = input('Input few first characters: ')
        if first_char == 'quit':
            break

        for _ in range(total_gen):
            gen = generate(model, vocab, first_char, max_length=mlength)
            print(f'Generated name: {gen}', end='\n')
        print('\n')