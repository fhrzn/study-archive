from torch import nn

class NameRNN(nn.Module):
    def __init__(self, vocab_size, out_size, hid_size=64, emb_size=32):
        super(NameRNN, self).__init__()

        # embedding layer is useful to map input into vector representation
        self.embedding = nn.Embedding(vocab_size, emb_size)

        # here we used RNN layer preserved by PyTorch library
        # that already handles RNN cell loops
        self.rnn = nn.RNN(emb_size, hid_size, batch_first=True)

        # Linear layer for output
        self.output = nn.Linear(hid_size, out_size)

    def forward(self, x):
        # here we only take input without previous hidden_state
        # bcs we let PyTorch define initial hidden_state for us

        # map input to vector
        x = self.embedding(x)

        # compute current hidden state
        # this layer returns output and hidden_state vector
        # but we'll take only the output vector
        o, _ = self.rnn(x)  

        # get last sequence output, bcs in this task we usually
        # want to take output vector from the very last sequence
        o = o[:, -1, :]     # (batch_size, seq_length, out_size)

        # feed output to linear layer
        out = self.output(o)

        return out


class NameLSTM(nn.Module):
    def __init__(self, vocab_size, out_size, hid_size=64, emb_size=32):
        super(NameLSTM, self).__init__()

        # embedding layer
        self.embedding = nn.Embedding(vocab_size, emb_size)

        # LSTM layer
        self.lstm = nn.LSTM(emb_size, hid_size, batch_first=True)

        # linear layer
        self.output = nn.Linear(hid_size, out_size)

    def forward(self, x):
        # map input to vector
        x = self.embedding(x)

        # compute current hidden state
        o, _ = self.lstm(x)

        # get last sequence output
        o = o[:, -1, :]

        # feed output to linear layer
        out = self.output(o)

        return out


class NameGRU(nn.Module):
    def __init__(self, vocab_size, out_size, hid_size=64, emb_size=32):
        super(NameGRU, self).__init__()

        # embedding layer
        self.embedding = nn.Embedding(vocab_size, emb_size)

        # GRU layer
        self.gru = nn.GRU(emb_size, hid_size, batch_first=True)

        # linear layer
        self.output = nn.Linear(hid_size, out_size)

    def forward(self, x):
        # map input to vector
        x = self.embedding(x)

        # compute current hidden state
        o, _ = self.gru(x)

        # get last sequence output
        o = o[:, -1, :]

        # feed output to linear layer
        out = self.output(o)

        return o