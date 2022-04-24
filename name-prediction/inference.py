import torch
from dataloader import encode_words, pad_features, load_data
import pickle
from constant import DEVICE, DATA_PATH, HID_SIZE, EMB_SIZE
from network import NameRNN, NameLSTM, NameGRU
from utils import output_to_label

def load_model(path):
    checkpoint = torch.load(path)
    return checkpoint

def predict(model, input, vocab):
    print(f'>>> {input}')

    with torch.no_grad():     
        # transform input to vector
        encoded = encode_words([input], vocab)
        # add padding with seq_length=20
        feature = torch.from_numpy(pad_features(encoded, seq_length=20))

        # move to device
        model = model.to(DEVICE)
        feature = feature.to(DEVICE)

        # forward pass
        out = model(feature)

    return out

if __name__ == '__main__':    

    # load vocab and labels
    print('Load vocab and labels...')    
    vocab = pickle.load(open('./models/vocab.pkl', 'rb'))
    labels = pickle.load(open('./models/labels.pkl', 'rb'))    

    # load model
    print('Load model checkpoint...')
    path = './models/name_rnnRNN.pt'
    model_weights = load_model(path)    

    # define network
    print('Apply checkpoints to model...')
    model = NameRNN(len(vocab), len(labels), HID_SIZE, EMB_SIZE)    
    model.load_state_dict(model_weights)

    # put model to eval mode
    model.eval()

    print('\n')

    # prompt user to input
    while True:
        name = input('Input name: ')
        if name == 'quit':
            break

        out = predict(model, name, vocab)        
        _, predicted = output_to_label(labels, out)
        print(f'Predicted Country: {predicted}', end='\n\n')