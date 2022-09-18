import spacy

nlp = spacy.load('en_core_web_sm')

# function that checks if an input sentence follows the word sequence pattern for dependency labels:
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


# function that checks if an input sentence follows the word sequence pattern for parts of speech:
# personal pronoun + modal verb + base form verb + ... + personal pronoun + ...
def pos_pattern(doc):
    for token in doc: 
        # subject of sentence is not a personal pronoun, pos sequence mismatch
        if token.dep_ == 'nsubj' and token.tag_ != 'PRP':
            return False
        # auxiliary verb of sentence is not modal, pos sequence mismatch
        if token.dep_ == 'aux' and token.tag_ != 'MD':
            return False
        # root verb of sentence is not in its base form, pos sequence mismatch
        if token.dep_ == 'ROOT' and token.tag_ != 'VB':
            return False
        # direct object of sentence is not a personal pronoun, pos sequence mismatch
        if token.dep_ == 'dobj' and token.tag_ != 'PRP':
            return False
    # no pos sequence mismatches, pos pattern matched
    return True


# finds any dobj in the submitted sentence, determines if the dobj is a personal pronoun, and then
# determines if the pronoun is singular or plural. 
# REMINDER: spaCy doesn't recognize pronouns as singular or plural by default
def pron_pattern(doc):
    plural = ['we', 'us', 'they', 'them']
    for token in doc:
        if token.dep_ == 'dobj' and token.tag_ == 'PRP':
            if token.text in plural:
                return 'plural'
            else: 
                return 'singular'
    return 'not found'


# finds the noun from a given text (sents) that matches a given personal pronoun
# sents may be made up of multiple sentences: it includes all sentences from a discourse up to
#      the sentence that satisfies dep_pattern and pos_pattern 
# if the personal pronoun is singular (she, he, I, etc.) then num = 'singular', and this function
#     will look for a singular noun 
# if the personal pronoun is plural (they, we, us, etc.) then num = 'plural', and this function 
#     will look for a plural noun
def find_noun(sents, num):
    if num == 'plural':
        taglist = ['NNS', 'NNPS']
    elif num == 'singular':
        taglist = ['NN', 'NNP']
    
    # we will search through the sentences in reverse order, because the noun we're searching for
    # is most likely in the sentences closely preceding the one with the personal pronoun 
    for sent in reversed(sents):
        for token in sent:
            if token.tag_ in taglist:
                # check if noun is preceded by an article
                for child in token.lefts:
                    if child.pos_ == 'DET' and child.tag_ == 'DT':
                        return child.text.lower() + ' ' + token.text.lower() # noun located, w/ article
                return token.text.lower()       # noun located, no article
    return 'Noun not found'             # noun not located


# replaces the direct object personal pronoun (dobj, PRP) token in a sentence with its 
#   corresponding noun, and generating a response to the given text (doc) 
def gen_utterance(doc, noun):
    sent = ''
    for i, token in enumerate(doc):
        if token.dep_ == 'dobj' and token.tag_ == 'PRP':
            # skip over the token and replace it with the noun
            sent = doc[:i].text + ' ' + noun + ' ' + doc[i+1:len(doc)-2].text + 'too.'
            return sent
    return 'Failed to generate an utterance'


doc = nlp('The symbols are clearly distinguishable. I can recognize them promptly.')

sents = list(doc.sents)
response = ''
noun = ''

for i, sent in enumerate(sents):
    # if a sentence matches both patterns
    if dep_pattern(sent) and pos_pattern(sent):
        # find noun corresponding to dobj PRP
        noun = find_noun(sents[:i], pron_pattern(sent))
        if noun != 'Noun not found':
            # generate response based on relevant sentence and corresponding noun
            response = gen_utterance(sents[i], noun)
            break
print(response)



