import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('I want to place an order for a pizza.')

# hardcoding a list of keywords is a viable practice in specific contexts in which the use of certain
# keywords is almost guaranteed. ex, if a customer is ordering from a pizza place, the use of the word
# "pizza" is almost guaranteed, as is "want". this is especially useful when the transitive verb/dobj
# pair does not accurately express intent

# find the transitive verb/dobj:
dobj = ''
tverb = ''
for token in doc:
    if token.dep_ == 'dobj':
        dobj = token
        tverb = token.head

# find intent verb for intent identification
verbList = ['want', 'like', 'need', 'order']
intentVerb = ''
# if the sentence's transitive verb is a keyword intent verb, intentVerb becomes the transitive verb
if tverb.text in verbList:
    intentVerb = tverb
else:
    if tverb.head.dep_ == 'ROOT':   # root verb becomes intentVerb
        intentVerb = tverb.head
        # if tverb is the ROOT verb, intentVerb will equal tverb


# find intent object for intent identification
objList = ['pizza', 'cola']
intentObj = ''
# if the sentence's dobj is a keyword intent obj, intentObj becomes the dobj
if dobj.text in objList:
    intentObj = dobj
else: 
    for child in dobj.children:
        if child.dep_ == 'prep':        # ex: for pizza || prep -> for
            intentObj = list(child.children)[0] # 'for'.children = [pizza]
            break
            # a preposition can only have 1 child, which is always the object of the prep
        elif child.dep_ == 'compound':  # ex: pizza order
            intentObj = child
            break

# print the intent expressed in the sample sentence
print(intentVerb.text + intentObj.text.capitalize())
