import spacy
from spacy.pipeline import DependencyParser

nlp = spacy.load('en_core_web_sm', disable=['parser'])
parser = DependencyParser(nlp.vocab)
parser.from_disk('/Users/adrie/AppData/Local/Programs/Python/Python38/lib/site-packages/en_core_web_sm/en_core_web_sm-2.3.1')

nlp.add_pipe(parser, "custom_parser")
print(nlp.meta['pipeline'])

doc = nlp('find a high paid job with no degree')
print([(token.text, token.dep_, token.head.text) for token in doc if token.dep_ != '-'])
# yay it works!!