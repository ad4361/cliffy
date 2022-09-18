"""
HUGE NOTE!!! at this point, I downloaded the most recent version of spacy. the examples from this
book used version 2.3.7, but this version was beginning to make a bunch of weird mistakes with 
lemmatizing and dependency parsing, so I finally switched over to the newest version. now it works.
so if anything in the chapters previous to this doesn't work, it's because of this version change.
To switch to version 2.3.7, enter the following into the Windows command prompts:
    -> py -m pip install spacy==2.3.7
    -> py -m spacy download en_core_web_sm
        (to download small statistical model for the version)
To switch to newest version of spacy, use the following commands:
    -> py -m pip install spacy
    -> py -m spacy download en_core_web_sm
"""

import spacy

nlp = spacy.load('en_core_web_sm')

doc = nlp('Do you know what an elephant eats?')
# 'elephant eats' is the keyphrase, which is nsubj + its verb
# note: the head of nsubj token is its verb
# note: we are reversing the doc because we want 'elephant eats', not 'you know'
phrase = ''
for token in reversed(doc):
    if token.dep_ == 'nsubj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
        phrase = token.text + ' ' + token.head.text
        break
print(phrase)
# phrase = 'elephant eats'


# sometimes, the verb/noun combo that forms the keyphrase is not the nsubj + its verb (like above)
# but instead is the transitive verb and its dobj
doc2  = nlp('How to feed a cat?')
# from this example, we want the phrase 'feeding cat'

phrase2 = ''
for token in reversed(doc2):
    if token.dep_ == 'dobj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
        phrase2 = token.head.lemma_ + 'ing ' + token.text
        break

print(phrase2)
# phrase2 = 'feeding cat'




# extract verb and its nsubj, as well as: 
#       -> any (non-determinant) modifiers of the nsubj
#       -> the direct object of the verb, if it has one
doc3 = nlp('Do you know how many eggs a sea turtle lays?')

phrase3 = ''
for token in reversed(doc3):
    if token.dep_ == 'nsubj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
        nsubj = token.text
        verb = token.head

        # nsubj's modifiers (non-determinant):
        modifiers = ' '.join([child.text for child in token.lefts if child.dep_ != 'det'])
        dobj = ''
        for child in verb.children:
            if child.dep_ == 'dobj':
                dobj = child.text
                break

        phrase3 = (modifiers + ' ' + nsubj + ' ' + verb.text + ' ' + dobj).lstrip()
        
print(phrase3)
# phrase3 = 'sea turtle lays eggs'



