import spacy
import wikipedia

nlp = spacy.load('en_core_web_sm')

doc = nlp('What do you know about rhinos?')

# iterate over utterance to find the first pobj (object of a preposition). the pobj is most likely
#       the keyword in the utterance
for token in doc:
    # make sure pobj is a noun or proper noun
    if token.dep_ == 'pobj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
        phrase = (' '.join([child.text for child in token.lefts]) + ' ' + token.text).lstrip()
        # phrase = 'rhinos', since pobj has no left children
        break # break means we only get first pobj and no other pobj in sentence

# wikipedia.page() function returns most relevant argument for a given keyword
print('Phrase: ' + phrase)
wiki_article = wikipedia.page(phrase)
print('Article title: ' +wiki_article.title)
print('Article url: ' + wiki_article.url)
print('Article summary: ' + wikipedia.summary(phrase, sentences=1) + '\n')

# above code prints:
# Article title: Rhinoceros
# Article url: https://en.wikipedia.org/wiki/Rhinoceros
# Article summary: A rhinoceros (; from Ancient Greek  ῥῑνόκερως (rhīnókerōs) 'nose-horned'; from  ῥῑνός 
#   (rhīnós) 'nose', and  κέρας (kéras) 'horn'), commonly abbreviated to rhino, is a member of any of the 
#   five extant species (or numerous extinct species) of odd-toed ungulates in the family Rhinocerotidae.




doc2 = nlp('Tell me about the color of the sky.')

for token in doc2:
    if token.dep_ == 'pobj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
        phrase = (' '.join([child.text for child in token.lefts]) + ' ' + token.text).lstrip()

        # check the pobj's right children. if one of them is a preposition, pick it up and its respective
        #       pobj, and add them to the phrase
        # bool() evaluates to True on non-empty lists
        if bool([rchild for rchild in token.rights if rchild.dep_ == 'prep']):
            prep = list(token.rights)[0]
            pobj = list(prep.children)[0]
            pobj_modifiers = (' '.join([child.text for child in pobj.lefts]))
            phrase_additions = prep.text + ' ' + pobj_modifiers + ' ' + pobj.text

            phrase = (phrase + ' ' + phrase_additions).rstrip()
        break

print('Phrase: ' + phrase)
wiki_article = wikipedia.page(phrase)
print('Article title: ' +wiki_article.title)
print('Article url: ' + wiki_article.url)
print('Article summary: ' + wikipedia.summary(phrase, sentences=1) + '\n')
