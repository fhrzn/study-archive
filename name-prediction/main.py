from network import NameRNN, NameGRU, NameLSTM
from dataloader import load
from train import train, test, plot_loss
import time
from InquirerPy import prompt
from constant import DATA_PATH, HID_SIZE, EMB_SIZE, EPOCH, LR, PRINT_EVERY, GRAD_CLIP, MODEL_PATH

if __name__ == '__main__':
    # load data and generate loader
    print('Load and generate DataLoader...')
    loader, vocab, labels = load(DATA_PATH)

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
        network = NameRNN(len(vocab), len(labels), HID_SIZE, EMB_SIZE)
    elif model_opt['model'] == 'LSTM':
        network = NameLSTM(len(vocab), len(labels), HID_SIZE, EMB_SIZE)
    elif model_opt['model'] == 'GRU':
        network = NameGRU(len(vocab), len(labels), HID_SIZE, EMB_SIZE)
    save_path = MODEL_PATH.format(model_opt['model'])

    # unpack loader
    train_loader, test_loader, val_loader = loader

    # train
    print('Training start...')
    start = time.time()
    model, history = train(network, train_loader, val_loader, EPOCH, LR, PRINT_EVERY, GRAD_CLIP, save_path)
    print(f'Training done. Time elapsed {time.time() - start:.2f} second.')
    
    # plot loss
    plot_loss(history)

    # inference on test set
    print('Inference on Test set.')
    test(model, test_loader)
