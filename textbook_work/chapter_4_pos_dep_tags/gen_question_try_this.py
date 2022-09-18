import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('I can promise it is worth your time.')

#for token in doc:
#    print(token.text, token.pos_, token.tag_, spacy.explain(token.tag_), token.dep_)
#print('\n')


# doc: discourse being manipulated
# replace: boolean, 
#   if true then a token is being replaced
#   if false, a token is being inserted or no token is being added to the sentence at all (inversion)
# tag: the fine-grained pos tag that is being searched for
# new_token: the new token that is being inserted or replaced; in case of inversion, None
# check_token: (when replace == true) the text of the token being replaced; if inversion, None
def generate_question(doc, replace, tag, new_token, check_token):
    sent = ''
    
    if tag == None:
        sent = doc[:len(doc)-1].text + '?'
        return sent
    
    if replace:
        for i, token in enumerate(doc):
            if token.tag_ == tag and token.text == check_token:
                sent = doc[:i].text + ' ' + new_token + ' ' + doc[i+1:].text
                return sent

    else: 
        if new_token != None:
            for i, token in enumerate(doc):
                if token.tag_ == tag:
                    sent = doc[:i].text + ' ' + new_token + ' ' + doc[i:].text
                    doc = nlp(sent)
                    return sent
        else:
            for i, token in enumerate(doc):
                # if personal pronoun + modal auxiliary verb + base form verb combo is seen:
                if token.tag_ == 'PRP' and doc[i+1].tag_ == 'MD' and doc[i+2].tag_ == 'VB':
                    # change it to modal auxiliary verb + personal pronoun + base form verb
                    sent = doc[i+1].text.capitalize() + ' ' + doc[i].text + ' ' + doc[i+2:].text + ' '
                    return sent


doc = nlp(generate_question(doc, False, 'PRP', None, None))
doc = nlp(generate_question(doc, True, 'PRP', 'you', 'I'))
doc = nlp(generate_question(doc, True, 'PRP$', 'my', 'your'))
doc = nlp(generate_question(doc, False, 'VB', 'really', None))
doc = nlp(generate_question(doc, False, None, None, None))

print(doc)

