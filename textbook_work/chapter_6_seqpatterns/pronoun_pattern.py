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


doc = nlp('We can overtake them.')
if dep_pattern(doc) and pos_pattern(doc):
    print('Pattern found: the pronoun in position of direct object is ' + pron_pattern(doc))
else:
    print('Pattern not found')


