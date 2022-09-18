# NOT necessary to import spacy for this example
from spacy import displacy

# manually generate a visualization without using a doc or span object (aka the spacy library)
# useful if you want to set custom dependency/tag labels, or if you want to see output from a
#   NLP library without having to download a huge file 


# using coarse-grained parts of speech
sent = {
    "words": [
        {"text": "I", "tag": "PRON"},
        {"text": "want", "tag": "VERB"},
        {"text": "a", "tag": "DET"},
        {"text": "Greek", "tag": "ADJ"},
        {"text": "pizza", "tag": "NOUN"}
    ],
    "arcs": [
        {"start": 0, "end": 1, "label": "nsubj", "dir": "left"},
        {"start": 2, "end": 4, "label": "det", "dir": "left"},
        {"start": 3, "end": 4, "label": "amod", "dir": "left"},
        {"start": 1, "end": 4, "label": "dobj", "dir": "right"}
    ]
}

# starts up server to view manual rendering in your browser
displacy.serve(sent, style='dep', manual=True)

# use ctrl C to close that server and boot up this following one


# using fine-grained parts of speech
sent2 = {
    "words": [
        {"text": "I", "tag": "PRP"},
        {"text": "want", "tag": "VBP"},
        {"text": "a", "tag": "DT"},
        {"text": "Greek", "tag": "JJ"},
        {"text": "pizza", "tag": "NN"}
    ],
    "arcs": [
        {"start": 0, "end": 1, "label": "nsubj", "dir": "left"},
        {"start": 2, "end": 4, "label": "det", "dir": "left"},
        {"start": 3, "end": 4, "label": "amod", "dir": "left"},
        {"start": 1, "end": 4, "label": "dobj", "dir": "right"}
    ]
}


# starts up server to view manual rendering in your browser
displacy.serve(sent2, style='dep', manual=True)
