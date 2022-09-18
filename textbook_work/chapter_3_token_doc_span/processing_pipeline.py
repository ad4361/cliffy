import spacy
nlp = spacy.load('en_core_web_sm')

# prints the names of the processing pipeline components for the nlp object
print(nlp.pipe_names)
# tagger: part of speech tagger
# parser: syntactic dependency parser
# ner: entity recognizer

print('\n')

# let's disable the parser, just to show we can:
nlp = spacy.load('en_core_web_sm', disable=['parser'])
doc = nlp('I want a green apple.')
for token in doc:
    print(token.text, token.pos_, token.dep_)
# since the parser was disabled, nothing will be printed for each token's dep_ field
