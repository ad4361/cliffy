import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('I can promise it is worth your time.')

#for token in doc:
#    print(token.text, token.pos_, token.tag_, spacy.explain(token.tag_), token.dep_)
#print('\n')


# we want to ask: Can you really promise it is worth my time?

sent = ''
for i, token in enumerate(doc):
    # if personal pronoun + modal auxiliary verb + base form verb combo is seen:
    if token.tag_ == 'PRP' and doc[i+1].tag_ == 'MD' and doc[i+2].tag_ == 'VB':
        # change it to modal auxiliary verb + personal pronoun + base form verb
        sent = doc[i+1].text.capitalize() + ' ' + doc[i].text + ' ' + doc[i+2:].text + ' '
        break

# sent = 'Can I promise it is worth your time'      # token replaced: DONE
doc = nlp(sent)
for i, token in enumerate(doc):
    if token.tag_ == 'PRP' and token.text == 'I':
        sent = doc[:i].text + ' you ' + doc[i+1:].text
        break

# sent = 'Can you promise it is worth your time.'       # token replaced: DONE
doc = nlp(sent)
for i, token in enumerate(doc):
    if token.tag_ == 'PRP$' and token.text == 'your':
        sent = doc[:i].text + ' my ' + doc[i+1:].text
        break

# sent = 'Can you promise it is worth my time.'         # token inserted
doc = nlp(sent)
for i, token in enumerate(doc):
    if token.tag_ == 'VB':
        sent = doc[:i].text + ' really ' + doc[i:].text
        break

# sent = 'Can you really promise it is worth my time.'
doc = nlp(sent)
sent = doc[:len(doc)-1].text + '?'
print(sent)
# Can you really promise it is worth my time?

# see gen_question_try_this.py for the function that can perform all of these operations
