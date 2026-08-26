KNOWN_DATASETS = [
    "ImageNet", "MNIST", "CIFAR-10", "CIFAR-100", "COCO", "SQuAD",
    "GLUE", "WikiText", "Common Crawl", "LibriSpeech", "Penn Treebank",
    "IMDB", "Cityscapes", "PASCAL VOC", "OpenWebText",
]

def extract_datasets(text):
    found = []
    for dataset in KNOWN_DATASETS:
        if dataset.lower() in text.lower():
            found.append(dataset)
    return found

import re

def extract_arxiv_citations(text):
    pattern = r"arXiv[:\s]*(\d{4}\.\d{4,5})"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return list(set(matches))

