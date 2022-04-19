import random
from dataprep import encodes
import torch
import os
import unicodedata
import random
from constant import ALL_LETTERS



def load_data(path):
    '''docstring'''

    def _to_ascii(text):
        '''docstring'''
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)\
                if unicodedata.category(c) != 'Mn' and c in ALL_LETTERS)

    names, labels = [], []
    all_labels = []
    files = os.listdir(path)

    for f in files:
        label = f.split('.')[0]
        all_labels.append(label)

        with open(path + f, encoding='utf-8') as r:
            # read each record
            lines = r.read().strip().split('\n')

            names.extend([_to_ascii(l) for l in lines])
            labels.extend([label for _ in range(len(lines))])

    # shuffle dataset
    index = list(range(len(names)))
    random.shuffle(index)
    names = [names[i] for i in index]
    labels = [labels[i] for i in index]
    
    return (names, labels), all_labels


def split(arr, split_size=.2):
    '''docstring'''
    # extract feature and label from tuple
    feature, label = arr

    # get index to split
    index = list(range(len(feature)))    
    index = random.sample(index, int(split_size * len(index)))    
    
    # make new feature and label
    feature_split = [feature[i] for i in index]
    label_split = [label[i] for i in index]
    
    # modify original feature and label    
    feature_new = [feature[i] for i, _ in enumerate(feature) if i not in index]
    label_new = [label[i] for i, _ in enumerate(label) if i not in index]

    return (feature_new, label_new), (feature_split, label_split)


# for now, we only implement single batch
def get_batches(arr, all_labels, batch_size=1):
    '''docstring'''

    features, targets = arr
    
    # preprocess
    features = encodes(features)
    # targets = [[torch.tensor([ALL_LETTERS.index(chr)]) for chr in t] for t in targets]    
    targets = [torch.tensor([all_labels.index(t)]) for t in targets]


    # make batches
    for i in range(0, len(features), batch_size):        
        ## if batch_size > 1 we need to use commented codes instead
        # feature = features[i:i+batch_size]
        # target = targets[i:i+batch_size]
        feature = features[i]
        target = targets[i]

        yield feature, target


if __name__ == '__main__':
    # sample feature and target
    feature = ['Hajime', 'Makarov']
    target = ['Japanese', 'Russian']
    # sample labels
    labels = ['Arabic',
            'Chinese',
            'Czech',
            'Dutch',
            'English',
            'French',
            'German',
            'Greek',
            'Irish',
            'Italian',
            'Japanese',
            'Korean',
            'Polish',
            'Portuguese',
            'Russian',
            'Scottish',
            'Spanish',
            'Vietnamese']
    
    # zipping feature target
    data = (feature, target)
    
    # get batch
    batch = get_batches(data, labels)
    # see our feature and target
    for f, t in batch:
        print(f'feature: {(f)}')
        print(f'target: {t}')