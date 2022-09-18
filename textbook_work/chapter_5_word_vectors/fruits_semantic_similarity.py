import spacy

nlp = spacy.load('en_core_web_lg')
token = nlp('fruits')[0] # create a token object for "fruits"

doc = nlp('I want to buy this beautiful book at the end of the week. Sales of citrus have increased over the last year. How much do you know about this type of tree?')

# compare "fruits" to each sentence in its entirety
for sent in doc.sents:
    print(sent)
    print('similarity to ' + token.text + ' is ' + str(token.similarity(sent)) + '\n')


# compare "fruits" to only the nouns in each sentence
similarity = {}
for i, sent in enumerate(doc.sents):
    noun_span_list = [sent[j].text for j in range(len(sent)) if sent[j].pos_ == 'NOUN']
    noun_span_str = ' '.join(noun_span_list)
    noun_span_doc = nlp(noun_span_str)
    similarity.update({i:token.similarity(noun_span_doc)})
print(similarity)
print('\n')
# with 'en_core_web_lg': {0: 0.21712277267612565, 1: 0.5007358123429245, 2: 0.3960727120792394}


# from the whole Doc object, see which individual noun has the highest semantic similarity to "fruits"
similarity = {}
for word in doc:
    if word.pos_ == 'NOUN':
        similarity.update({word.text:word.similarity(token)})
print(similarity)
# with 'en_core_web_lg':
# {'book': 0.14252521, 'end': 0.21482901, 'week': 0.15574455, 'Sales': 0.15785275, 
# 'citrus': 0.638938, 'year': 0.16159745, 'type': 0.21295437, 'tree': 0.41544825}
# we can see that 'citrus' is the noun with the greatest semantic similarity to 'fruits', with 
# tree following behind. makes sense







