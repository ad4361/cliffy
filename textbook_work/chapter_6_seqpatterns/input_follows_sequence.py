import spacy
nlp = spacy.load('en_core_web_sm')


# function that checks if an input sentence follows the word sequence pattern:
# subject + auxiliary verb + verb + ... + direct object + ...
def dep_pattern(doc):
    # iterate over sentence, excluding end mark:
    for i in range(len(doc)-1):
        # if subject + auxiliary verb + verb detected:
        if doc[i].dep_ == 'nsubj' and doc[i+1].dep_ == 'aux' and doc[i+2].dep_ == 'ROOT':
            # if verb has a direct object child, return True
            for token in doc[i+2].rights:
                if token.dep_ == 'dobj':
                    return True
        # if pattern not matched, return False
        return False

doc1 = nlp('We can overtake them.')
doc2 = nlp('I might send them a card as a reminder.')
doc3 = nlp('I want to order a vegetarian pizza.')

if dep_pattern(doc1):
    print('Input matches pattern')
else:
    print('Input does not match pattern')

if dep_pattern(doc2):
    print('Input matches pattern')
else:
    print('Input does not match pattern')

if dep_pattern(doc3):
    print('Input matches pattern')
else:
    print('Input does not match pattern')