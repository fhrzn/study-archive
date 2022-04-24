import torch

def output_to_label(labels, output):
    label_id = torch.argmax(output).item()
    return label_id, labels[label_id]