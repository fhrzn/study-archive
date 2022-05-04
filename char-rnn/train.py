import torch
from torch.optim import Adam
from torch import nn
from constant import ES, DEVICE, MODEL_PATH
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

def train(model, trainloader, valloader=None, epochs=500, lr=.001, print_every=100, grad_clip=5, save_path=MODEL_PATH.format('')):

    # dict to store training logs
    history = {
        'train_loss': [],
        'val_loss': [],
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
    epochloop = tqdm(range(epochs), position=0, desc='Training', leave=True)

    for e in epochloop:

        #################
        # training mode #
        #################

        model.train()

        # running loss
        train_loss = 0

        for feature in trainloader:
            # transform datatype
            feature = feature[0]
            feature = feature.type(torch.LongTensor)

            # move to device
            feature = feature.to(DEVICE)

            # reset optimizer
            optim.zero_grad()

            # forward pass
            out, _ = model(feature)
            pred = out[:, :-1]
            actual = feature[:, 1:]

            # compute loss
            # example:
            # input = 'maxim'
            # out     = ['m', 'a', 'x', 'i']
            # feature = ['a', 'x', 'i', 'm']
            loss = criterion(pred.contiguous().view(-1, model.vocab_size),
                             actual.contiguous().view(-1))

            #  backpropagate
            loss.backward()

            # clip gradient
            nn.utils.clip_grad_norm_(model.parameters(), grad_clip)

            # update optimizer
            optim.step()

            # write loss
            train_loss += loss.item()

        # write history loss
        history['train_loss'].append(train_loss / len(trainloader))


        ####################
        # validation model #
        ####################

        model.eval()

        # eval loss
        val_loss = 0

        with torch.no_grad():
            for feature in valloader:
                # transform datatype
                feature = feature[0].type(torch.LongTensor)

                # move to device
                feature = feature.to(DEVICE)

                # forward pass
                out, _ = model(feature)
                pred = out[:, :-1]
                actual = feature[:, 1:]

                # compute loss
                loss = criterion(pred.contiguous().view(-1, model.vocab_size),
                                 actual.contiguous().view(-1))

                # write loss
                val_loss += loss.item()

        # write loss history
        history['val_loss'].append(val_loss / len(valloader))

        # put back model to train mode
        model.train()

        # add epoch meta info
        epochloop.set_postfix_str(f'Val Loss: {val_loss / len(valloader):.3f}')

        # print epoch
        if (e+1) % print_every == 0 or e == 0:
            epochloop.write(f'Epoch {e+1}/{epochs} | Train Loss: {train_loss/len(trainloader):.4f} | Val Loss: {val_loss/len(valloader):.4f}')
            epochloop.update()

            # save model if validation loss decrease
            if val_loss / len(valloader) <= val_loss_min:
                torch.save(model.state_dict(), save_path)
                val_loss_min = val_loss / len(valloader)
                es_trigger = 0
            else:
                epochloop.write(f'[WARNING] Loss did not improving ({val_loss_min:.4f} --> {val_loss/len(valloader):.4f})')
                es_trigger += 1

            # force early stop
            if es_trigger >= 5:
                epochloop.write(f'Early stopped at Epoch-{e}')
                # update epochs history
                history['epochs'] = e+1
                break

    return model, history    

def plot_loss(history):
    # history loss
    plt.figure(figsize=(6, 8))
    plt.plot(range(history['epochs']), history['train_loss'], label='Train Loss')
    plt.plot(range(history['epochs']), history['val_loss'], label='Val Loss')
    plt.legend()
    plt.savefig('./plot/loss_history.png', format='png')