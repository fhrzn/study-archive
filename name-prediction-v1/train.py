import torch
from torch.optim import Adam
from torch import nn
from tqdm import tqdm
from dataloader import get_batches
from utils import output_to_label
from constant import LOG_LEVEL, MODEL_NAME, EARLY_STOP

def training(model, all_labels, train_data, val_data, device, epochs=1000, lr=.05, print_every=100, log_every=100):
    '''docstring'''

    # set model to train mode
    model.train()
    # define optimizer
    optimizer = Adam(model.parameters(), lr=lr)
    # define loss function
    criterion = nn.NLLLoss()

    # move to device (either CPU/GPU)
    model.to(device)

    # define loss and acc
    train_loss, val_loss = [], []
    train_acc, val_acc = [], []
    # define early stop trigger
    es_trigger = 0

    # validation loss minimum
    val_loss_min = torch.inf

    for e in tqdm(range(epochs), desc='Epoch', ncols=75):
        ####################
        # Training Section #
        ####################


        # define local loss and acc
        tloss = 0
        tacc = []

        # load our batch data
        for tid, (feature, target) in enumerate(get_batches(train_data, all_labels)):
            # init hidden state
            hidden = model.init_hidden(device)

            # move our feature, hidden state and target to gpu
            feature, hidden, target = feature.to(device), hidden.to(device), target.to(device)

            # reset optimizer
            optimizer.zero_grad()

            # forward pass for each char sequences
            for row in feature:
                # add dimension to feature
                row = row.view(1, -1)
                # forward pass and update our hidden state
                output, hidden = model(row, hidden)

            # compute loss
            loss = criterion(output, target)            
            # record local loss       
            tloss += loss.item()
            # compute accuracy
            label_id, predicted = output_to_label(all_labels, output)
            # record local acc
            tacc.append(1 if label_id == target else 0)

            # reset local loss
            if tid % log_every == 0:
                if LOG_LEVEL == 'DEBUG':
                    tqdm.write(f'Tloss: {tloss} - Tloss final: {tloss/log_every}')
                train_loss.append(tloss/log_every)
                tloss = 0

            # backpropagation
            loss.backward()
            # update weights
            optimizer.step()
        
        train_acc.append(sum(tacc)/len(tacc))


        ######################
        # Validation Section #
        ######################
        

        # define local loss and acc
        vloss = 0
        vacc = []

        # set model to eval mode
        model.eval()

        # we turned off gradient on validation mode
        # we also won't perform backpropagation and optimization
        with torch.no_grad():
            # load our batch data
            for vid, (feature, target) in enumerate(get_batches(val_data, all_labels)):
                # init hidden state
                hidden = model.init_hidden(device)

                # move our feature, hidden state and target to gpu
                feature, hidden, target = feature.to(device), hidden.to(device), target.to(device)

                # forward pass for each char sequences
                for row in feature:
                    # add dimension to feature
                    row = row.view(1, -1)
                    # forward pass and update our hidden state
                    output, hidden = model(row, hidden)

                # compute loss
                loss = criterion(output, target)
                # record local loss                
                vloss += loss.item()
                # compute accuracy
                label_id, predicted = output_to_label(all_labels, output)
                # record local acc
                vacc.append(1 if label_id == target else 0)

                if vid % log_every == 0:
                    val_loss.append(vloss/log_every)
                    vloss = 0
                        
            val_acc.append(sum(vacc)/len(vacc))

        # reset model to train mode
        model.train()

        # print epoch
        if (e+1) % print_every == 0:
            tqdm.write(f"Epoch-{e} | Loss: {sum(train_loss)/len(train_loss):.4f} Acc: {sum(train_acc)/len(train_acc)} | Val Loss: {sum(val_loss)/len(val_loss):.4f} - Acc: {sum(val_acc)/len(val_acc)}")
                
        # save model if validation loss decrease
        if sum(val_loss)/len(val_loss) <= val_loss_min:
            torch.save(model.state_dict(), MODEL_NAME)
            val_loss_min = sum(val_loss) / len(val_loss)
            es_trigger = 0
        else:
            tqdm.write(f'[WARNING] Validation loss not improving ({val_loss_min:.4f} --> {sum(val_loss)/len(val_loss):.4f})')
            es_trigger += 1

        if es_trigger >= EARLY_STOP:
            tqdm.write(f'Early stopped at Epoch-{e}')
            break

    return train_loss, val_loss, train_acc, val_acc