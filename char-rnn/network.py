from torch import nn

# network architecture
class RNNNameGenerator(nn.Module):
    def __init__(self, vocab_size, hidden_size, embedding_size=32, dropout=0.2, char2int=None, int2char=None):
        super(RNNNameGenerator, self).__init__()

        # useful model properties
        self.vocab_size = vocab_size        
        self.char2int = char2int
        self.int2char = int2char

        # embedding layer is useful to map input into vector representation
        self.embedding = nn.Embedding(vocab_size, embedding_size)

        # RNN layer preserved by PyTorch library
        # this layer handles RNN Cell loops
        self.rnn = nn.RNN(embedding_size, hidden_size, batch_first=True)

        # Linear layer for output
        self.output = nn.Linear(hidden_size, vocab_size)

        # Dropout layer
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, h=None):
        # its optional to init hidden state by ourselves
        # bcs PyTorch will handle it if we don't provide it

        # map input to vector
        x = self.embedding(x)

        # compute current hidden state
        o, h = self.rnn(x, h)

        # apply dropout
        o = self.dropout(o)

        # compute output
        o = self.output(o)

        # here we return hidden state too cz we want to use it in inference mode
        return o, h


# network architecture
class LSTMNameGenerator(nn.Module):
    def __init__(self, vocab_size, hidden_size, embedding_size=32, dropout=0.2, char2int=None, int2char=None):
        super(LSTMNameGenerator, self).__init__()

        # useful model properties
        self.vocab_size = vocab_size        
        self.char2int = char2int
        self.int2char = int2char

        # embedding layer is useful to map input into vector representation
        self.embedding = nn.Embedding(vocab_size, embedding_size)

        # LSTM layer preserved by PyTorch library
        # this layer handles LSTM Cell loops
        self.lstm = nn.LSTM(embedding_size, hidden_size, batch_first=True)

        # Linear layer for output
        self.output = nn.Linear(hidden_size, vocab_size)

        # Dropout layer
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, h=None):
        # its optional to init hidden state by ourselves
        # bcs PyTorch will handle it if we don't provide it

        # map input to vector
        x = self.embedding(x)

        # compute current hidden state
        o, h = self.lstm(x, h)

        # apply dropout
        o = self.dropout(o)

        # compute output
        o = self.output(o)

        # here we return hidden state too cz we want to use it in inference mode
        return o, h


# network architecture
class GRUNameGenerator(nn.Module):
    def __init__(self, vocab_size, hidden_size, embedding_size=32, dropout=0.2, char2int=None, int2char=None):
        super(GRUNameGenerator, self).__init__()

        # useful model properties
        self.vocab_size = vocab_size        
        self.char2int = char2int
        self.int2char = int2char

        # embedding layer is useful to map input into vector representation
        self.embedding = nn.Embedding(vocab_size, embedding_size)

        # GRU layer preserved by PyTorch library
        # this layer handles GRU Cell loops
        self.gru = nn.GRU(embedding_size, hidden_size, batch_first=True)

        # Linear layer for output
        self.output = nn.Linear(hidden_size, vocab_size)

        # Dropout layer
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, h=None):
        # its optional to init hidden state by ourselves
        # bcs PyTorch will handle it if we don't provide it

        # map input to vector
        x = self.embedding(x)

        # compute current hidden state
        o, h = self.gru(x, h)

        # apply dropout
        o = self.dropout(o)

        # compute output
        o = self.output(o)

        # here we return hidden state too cz we want to use it in inference mode
        return o, h