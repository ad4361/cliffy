import spacy
nlp = spacy.load('en_core_web_sm')

doc = nlp('Kiwano has jelly-like flesh with a refreshingly fruity taste. This is a nice exotic fruit from Africa. It is definitely worth trying.')

fruit_adjectives = []
fruit_origins = []

for token in doc:
    if token.text == 'fruit':
        # add adjectives to the left of fruit to fruit_adjectives
        fruit_adjectives = fruit_adjectives + [modifier.text for modifier in token.lefts if modifier.pos_ == 'ADJ']
        # add entity name to fruit_origins if the entity is preceded by "from"
        fruit_origins = fruit_origins + [doc[modifier.i+1].text for modifier in token.rights if modifier.text == 'from' and doc[modifier.i+1].ent_type != 0]  
print('The list of adjectival modifiers for the word \'fruit\':', fruit_adjectives)
print('The list of GPE names applicable to the word \'fruit\' as postmodifiers:', fruit_origins)


