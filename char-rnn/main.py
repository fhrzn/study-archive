from network import RNNNameGenerator, LSTMNameGenerator, GRUNameGenerator
from dataloader import load
from train import train, plot_loss
import time
from InquirerPy import prompt
from constant import DATA_PATH, HID_SIZE, EMB_SIZE, EPOCH, LR, PRINT_EVERY, GRAD_CLIP, MODEL_PATH

if __name__ == '__main__':

    # load data and generate loader
    print('Load and generate DataLoader...')
    loader, vocab, int2char = load(DATA_PATH)

    # prompt model selection
    questions = [
        {
            'type': 'list',
            'message': 'Choose model options',
            'choices': ['RNN', 'LSTM', 'GRU'],
            'name': 'model'
        }
    ]
    model_opt = prompt(questions)

    # init model
    print('Initializing model...')
    # model init
    if model_opt['model'] == 'RNN':
        network = RNNNameGenerator(len(vocab), HID_SIZE, EMB_SIZE, char2int=vocab, int2char=int2char)
    elif model_opt['model'] == 'LSTM':
        network = LSTMNameGenerator(len(vocab), HID_SIZE, EMB_SIZE, char2int=vocab, int2char=int2char)
    elif model_opt['model'] == 'GRU':
        network = GRUNameGenerator(len(vocab), HID_SIZE, EMB_SIZE, char2int=vocab, int2char=int2char)
    save_path = MODEL_PATH.format(model_opt['model'])

    # unpack loader
    trainloader, testloader = loader

    # train
    print('Training start...')
    start = time.time()
    model, history = train(network, trainloader, testloader, EPOCH, LR, PRINT_EVERY, GRAD_CLIP, save_path)
    print(f'Training done. Time elapsed {time.time() - start:.2f} second.')

    # plot loss
    plot_loss(history)    