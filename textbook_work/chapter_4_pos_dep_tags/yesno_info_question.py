import spacy
import sys


# analyzes a given sentence and returns the noun chunk that forms the direct object of a verb
# (if there is a dobj)
def find_dobj_nounchunk(doc):
    chunk = ''
    for i, token in enumerate(doc):
        if token.dep_ == 'dobj':
            # create array of token's syntactic children to see the length of the array
            # len(token.children) isn't valid, which is why this is necessary
            shift = len([w for w in token.children])
            
            # 0  1   2   3     4  5
            # I want a green apple.
            
            chunk = doc[i-shift:i+1]
            # with above example, chunk = doc[4-2:4+1]
            #                     chunk = doc[2:5]
            #                     chunk = 'a green apple'
            break
    return chunk


# analyzes a given noun chunk and determines what question type to ask:
#       if adjectival modifier present: info question
#       if amod absent: yesno 
def determine_question_type(chunk):
    question_type = 'yesno'
    for token in chunk:
        if token.dep_ == 'amod':
            question_type = 'info'
    return question_type



def generate_question(doc, question_type):
    # example sentence: I want a green apple.
    sent = ''
    for i, token in enumerate(doc):
        # VBP: verb, non-3rd person singular present (ex: I **want**)
        # case: no modal auxiliary verb
        if token.tag_ == 'PRP' and doc[i+1].tag_ == 'VBP':
            sent = 'do ' + doc.text
            # ex: do I want a green apple.
            break
        
        # case: personal pronoun + modal auxiliary verb + base form verb combo is seen:
        elif token.tag_ == 'PRP' and doc[i+1].tag_ == 'MD' and doc[i+2].tag_ == 'VB':
            # change it to modal auxiliary verb + personal pronoun + base form verb
            sent = doc[i+1].text + ' ' + doc[i].text + ' ' + doc[i+2:].text + ' '
            # ex: might I want a green apple.
            break
    doc = nlp(sent)
    
    for i, token in enumerate(doc):
        # replace first instance of 'I' with 'you'
        if token.tag_ == 'PRP' and token.text == 'I':
            sent = doc[:i].text + ' you ' + doc[i+1:].text
            # ex: do you want a green apple.
            # ex: might you want a green apple.
            break
    doc = nlp(sent)

    # who/what/when/where/why/how
    if question_type == 'info':
        for i, token in enumerate(doc):
            if token.dep_ == 'dobj':
                sent = 'why ' + doc[:i].text + ' one ' + doc[i+1:].text
                # ex: why do you want a green one.
                # ex: why might you want a green one.
                break
    
    elif question_type == 'yesno':
        # ex: do you want an apple.
        # ex: might you want an apple.
        for i, token in enumerate(doc):
            if token.dep_ == 'dobj':
                sent = doc[:i-1].text + ' a red ' + doc[i:].text
                # ex: do you want a red apple.
                # ex: might you want a red apple.
                break
    doc = nlp(sent)
    sent = doc[0].text.capitalize() + ' ' + doc[1:len(doc)-1].text + '?'
    # ex: Do you want a red apple?
    # ex: Why do you want a green one?
    return sent


# argv[0] is the script name, if one is given
if len(sys.argv) > 1:
    nlp = spacy.load('en_core_web_sm')
    
    sent = sys.argv[1]
    doc = nlp(sent)
    
    chunk = find_dobj_nounchunk(doc)
    if str(chunk) == '':
        print('The sentence does not contain a direct object.')
        sys.exit()
    question_type = determine_question_type(chunk)
    question = generate_question(doc, question_type)
    print(question)
else:
    print('Please submit a sentence.')


