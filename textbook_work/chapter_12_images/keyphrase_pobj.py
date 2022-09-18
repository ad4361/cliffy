import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('Tell me about World War II.')

# iterate over utterance to find the first pobj (object of a preposition). the pobj is most likely
#       the keyword in the utterance
for token in doc:
    # make sure pobj is a noun or proper noun
    if token.dep_ == 'pobj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
        phrase = (' '.join([child.text for child in token.lefts]) + ' ' + token.text).lstrip()
        # phrase = 'rhinos', since pobj has no left children
        break # break means we only get first pobj and no other pobj in sentence

print(phrase)

# in the above scenario, the keyphrase of the sentence involved only one prepositional object.
# this won't always be the case, such as with: 'Tell me about the color of the sky.'
# solution: pick up any pobj that follows the first pobj, provided that the first pobj is dependent
#       on the ones that follow it (i.e. 'color' depends on 'sky')

doc2 = nlp('Tell me about the color of the sky.')

for token in doc2:
    if token.dep_ == 'pobj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
        phrase = (' '.join([child.text for child in token.lefts]) + ' ' + token.text).lstrip()

        # check the pobj's right children. if one of them is a prepositon, pick it up and its respective
        #       pobj, and add them to the phrase
        # bool() evaluates to True on non-empty lists
        if bool([rchild for rchild in token.rights if rchild.dep_ == 'prep']):
            prep = list(token.rights)[0]
            pobj = list(prep.children)[0]
            phrase = phrase + ' ' + prep.text + ' ' + pobj.text
        break

print(phrase)
# prints 'the color of sky'