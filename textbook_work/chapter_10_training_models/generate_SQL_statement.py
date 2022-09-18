import spacy

# need semantic parser that we trained in create_semantic_parser.py
from spacy.pipeline import DependencyParser

nlp = spacy.load('en_core_web_sm', disable=['parser'])
parser = DependencyParser(nlp.vocab)
parser.from_disk('/Users/adrie/AppData/Local/Programs/Python/Python38/lib/site-packages/en_core_web_sm/en_core_web_sm-2.3.1')
nlp.add_pipe(parser, "custom_parser")

doc = nlp(u'find a high paid job with no degree')
#for token in doc:
#    if token.dep_ != '-':
#       print(token.text, token.dep_, token.head.text)

# SELECT * FROM jobs WHERE salary = 'high' AND experience = 'no'
# ROOT -> SELECT
# ACTIVITY -> table name
# QUALITY/ATTRIBUTE: WHERE
SQL_str = ''
root = ''
activity = ''
token_attr = {}
for token in doc:
    # save root token to variable
    if token.dep_ == 'ROOT':
        root = token.text
    
    # save activity token to variable
    elif token.dep_ == 'ACTIVITY':
        activity = token.text
        #add entry for activity to token_attr dictionary, if not already present
        if activity not in token_attr:
            token_attr[activity] = []
    
    elif token.dep_ == 'ATTRIBUTE':
        #add entry for attribute to token_attr dictionary, if not already present
        if token.text not in token_attr:
            token_attr[token.text] = []

    # QUALITYs can describe either an ATTRIBUTE or ACTIVITY
    elif token.dep_ == 'QUALITY':
        quality = token.text
        head = token.head.text
        
        if head not in token_attr:
            token_attr[head] = []

        token_attr[head].append(quality)

# at the time of coding, spacy's lemmatizer isn't working for en_core_web_sm model, so this list is necessary
salary_words = ['pay', 'paying', 'paid', 'pays']

# start assembling SQL query string
# this may be the worst code I've ever written. makes lots of ridiculous assumptions
if root == 'find' or root == 'show':
    SQL_str = 'SELECT * FROM '
    if activity:
        SQL_str += activity + 's '
        if len(token_attr[activity]) != 0 or len(token_attr) > 1:
            SQL_str += 'WHERE '
            if len(token_attr[activity]) != 0:
                for attr in token_attr[activity]:
                    if attr in salary_words and len(token_attr[activity]) > 1:
                        SQL_str += 'salary = \''
                        token_attr[activity].remove(attr)
                        SQL_str += token_attr[activity][0] + '\''
            if len(token_attr) > 1:
                for key in token_attr:
                    if key == activity:
                        pass
                    else:
                        SQL_str += ' AND ' + key + ' = \'' + token_attr[key][0] + '\''

print(SQL_str)
# SELECT * FROM jobs WHERE salary = 'high' AND degree = 'no'
# this is awful code but I wanna move on now


