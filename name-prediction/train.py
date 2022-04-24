import torch
from torch.optim import Adam
from torch import nn
from constant import ES, DEVICE, MODEL_PATH
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

def train(model, train_loader, val_loader, epochs=500, lr=.001, print_every=100, grad_clip=5, save_path=MODEL_PATH.format('')):

    # dict to store training logs
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': [],
        'epochs': epochs
    }

    # move model to GPU (if available)
    model = model.to(DEVICE)

    # define optimizer and loss
    optim = Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    # early stop trigger
    es_trigger = 0
    val_loss_min = torch.inf

    # setup epoch tqdm
    epochloop = tqdm(range(epochs), position=0, desc='Training...', leave=True)

    for e in epochloop:

        #################
        # training mode #
        #################

        model.train()

        # running train loss and acc
        train_loss = 0
        train_acc = 0

        for feature, target in train_loader:
            
            # convert target type to Long
            target = target.type(torch.LongTensor)

            # move to device
            feature, target = feature.to(DEVICE), target.to(DEVICE)

            # reset optimizer
            optim.zero_grad()

            # forward pass
            out = model(feature)

            # compute acc
            predicted = torch.argmax(out, dim=1) == target
            acc = torch.mean(predicted.type(torch.FloatTensor))
            train_acc += acc.item()

            # compute loss
            loss = criterion(out, target)
            train_loss += loss.item()
            
            # backpropagate
            loss.backward()

            # clip grad
            nn.utils.clip_grad_norm_(model.parameters(), grad_clip)

            # update optimizer
            optim.step()

        # record train history
        history['train_loss'].append(train_loss / len(train_loader))
        history['train_acc'].append(train_acc / len(train_loader))


        ###################
        # validation mode #
        ###################

        model.eval()

        # running val loss and acc
        val_loss = 0
        val_acc = 0

        # turn off gradient
        with torch.no_grad():
            for feature, target in val_loader:

                # convert target type to Long
                target = target.type(torch.LongTensor)

                # move to device
                feature, target = feature.to(DEVICE), target.to(DEVICE)

                # forward pass
                out = model(feature)

                # compute acc
                predicted = torch.argmax(out, dim=1) == target
                acc = torch.mean(predicted.type(torch.FloatTensor))
                val_acc += acc.item()

                # compute loss
                loss = criterion(out, target)
                val_loss += loss.item()

        # record validation history
        history['val_loss'].append(val_loss / len(val_loader))
        history['val_acc'].append(val_acc / len(val_loader))

        # reset model mode
        model.train()

        # add epoch meta info
        epochloop.set_postfix_str(f'Val Loss: {val_loss/len(val_loader):.3f}')

        # print epoch
        if (e+1) % print_every == 0:
            epochloop.write(f'Epoch {e+1}/{epochs} | Train Loss: {train_loss/len(train_loader):.4f} | Val Loss: {val_loss/len(val_loader):.4f} Acc: {val_acc/len(val_loader):.4f}')
            epochloop.update()

        # save model if validatoin loss decrease
        if val_loss/len(val_loader) <= val_loss_min:            
            torch.save(model.state_dict(), save_path)
            val_loss_min = val_loss/len(val_loader)
            es_trigger = 0
        else:
            epochloop.write(f'[WARNING] Validation loss not improving ({val_loss_min:.4f} --> {val_loss/len(val_loader):.4f})')
            es_trigger += 1

        # force early stop
        if es_trigger >= ES:
            epochloop.write(f'Early stopped at Epoch-{e}')
            # update epochs history
            history['epochs'] = e+1
            break        
    
    return model, history

def test(model, test_loader):
    ###################
    # validation mode #
    ###################

    model.eval()

    # loss function
    criterion = nn.CrossEntropyLoss()

    # test loss and acc
    test_loss = 0
    test_acc = 0

    # setup test_loader tqdm
    testloop = tqdm(test_loader, position=0, leave=True, desc='Inference on test data...')

    # turn off gradient
    with torch.no_grad():
        for feature, target in testloop:

            # convert target type to Long
            target = target.type(torch.LongTensor)

            # move to device
            feature, target = feature.to(DEVICE), target.to(DEVICE)

            # forward pass
            out = model(feature)

            # compute acc
            predicted = torch.argmax(out, dim=1) == target
            acc = torch.mean(predicted.type(torch.FloatTensor))
            test_acc += acc.item()

            # compute loss
            loss = criterion(out, target)
            test_loss += loss.item()

    print(f'Accuracy: {test_acc/len(test_loader)}, Loss: {test_loss/len(test_loader)}')

def plot_loss(history):
    # history loss
    plt.figure(figsize=(6,8))
    plt.plot(range(history['epochs']), history['train_loss'], label='Train Loss')
    plt.plot(range(history['epochs']), history['val_loss'], label='Val Loss')
    plt.legend()
    plt.savefig('./plot/loss_history.png', format='png')

    # history  acc
    plt.figure(figsize=(6, 8))
    plt.plot(range(history['epochs']), history['train_acc'], label='Train Acc')
    plt.plot(range(history['epochs']), history['val_acc'], label='Val Acc')
    plt.legend()
    plt.savefig('./plot/acc_history.png', format='png')