from torch import nn
import torch
# for testing purpose
from dataloader import load_data
from dataprep import one_hot_encode
from constant import DATA_PATH, N_LETTERS
from utils import output_to_label

class NameRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(NameRNN, self).__init__()

        self.hidden_size = hidden_size
        
        # from input layer to hidden layer
        self.layer_hidden = nn.Linear(input_size + hidden_size, hidden_size)
        
        # from input layer to outpu layer
        self.layer_output = nn.Linear(input_size + hidden_size, output_size)

        # softmax activation bcs we want multiclass classification
        self.softmax = nn.LogSoftmax(dim=1)

    
    def forward(self, input_tensor, hidden_tensor):
        # combine input and hidden
        combined = torch.cat((input_tensor, hidden_tensor), dim=1)

        # forward pass to hidden layer
        hidden = self.layer_hidden(combined)
        # forward pass to output layer
        output = self.layer_output(combined)
        
        # softmax activation
        output = self.softmax(output)

        return output, hidden

    
    def init_hidden(self, device):
        return torch.zeros((1, self.hidden_size), device=device)

    


if __name__ == '__main__':

    # let's get all labels/classes
    _, labels = load_data(DATA_PATH)
    n_categories = len(labels)
    
    # define hidden size
    hidden_size = 128
    
    # model initialization
    network = NameRNN(N_LETTERS, hidden_size, n_categories)
    # get network architecture    
    print(network)

    # our dummy input
    input_tensor = one_hot_encode('Abbas')
    # init hidden tensor
    hidden_tensor = network.init_hidden()

    # so here we will treat input as sequences
    # that's why we need to iterate each row and pass to network
    for row in input_tensor:        
        # our row dimension is like [[55]]
        # while our hidden_tensor is like [[1, 128]]
        # so we'll add dimension and our row will become [[1, 55]]
        row = row.reshape(1, -1)
        
        # forward pass for each one-hot encoded sequences
        output, hidden = network(row, hidden_tensor)

    print(f'Name: Abbas -> Predicted label: {output_to_label(labels, output)}')