import spacy
from db_IGNORE import dbpass

nlp = spacy.load('en_core_web_sm')
doc = nlp('I want a Greek pizza.')
#doc = nlp('I want two pizzas.')
#doc = nlp('I want Greek pizzas.')


# Function that will convert a string number modifier into an integer 
# String can be a word (four) or digit (4)
def word2int(numword):
    num = 0
    # use try/except block (similar to Java try/catch block)
    try:
        num = int(numword)
        return num # if numword is a digit, this will execute
    except ValueError:  # will execute if numword is a string
        pass
    
    words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen',
    'nineteen', 'twenty']

    # find which word in the above list matches the numword argument, and return the word's index
    for i, word in enumerate(words):
        if numword == word:
            num = i
    
    return num



# create dictionary that will hold the structured data taken from doc object
# oderDict is the container for the JSON object being created
orderDict = {}

for token in doc:
    # search for dobj of utterance, which will be the JSON object's "product"
    if token.dep_ == 'dobj':
        dobj = token
        orderDict.update(product = dobj.lemma_) # lemmatize the dobj before adding it to JSON object

        for child in dobj.lefts:
            if child.dep_ == 'amod' or child.dep_ == 'compound':
                orderDict.update(ptype = child.text)
            elif child.dep_ == 'det':
                orderDict.update(qty = 1)
            elif child.dep_ == 'nummod':
                orderDict.update(qty = word2int(child.text))

print(orderDict)
# prints the string that is the conversion of the JSON object to a JSON string
# this string is what we send to the database


# connect to the database and pass the order data to our underlying database
import json
import mysql.connector
from mysql.connector import errorcode

# convert orderDict to JSON string
json_str = json.dumps(orderDict) # JSON string from order
try:
    cnx = mysql.connector.connect(user='root', password=dbpass,
        host='127.0.0.1', database='mybot')
    query = (""" INSERT INTO orders (product, ptype, qty)
    SELECT product, ptype, qty FROM
        JSON_TABLE(
            %s,
            "$" COLUMNS(
                qty     INT PATH '$.qty' ERROR ON EMPTY,
                product VARCHAR(30) PATH "$.product" ERROR ON EMPTY,
                ptype   VARCHAR(30) PATH "$.ptype" ERROR ON EMPTY
            )
        ) AS jt1""")
    cursor = cnx.cursor()
    cursor.execute(query, (json_str,)) # json_str is bound to the %s argument in JSON_TABLE
    # customer's order is inserted into our table in our database
    cnx.commit() # commits the above statement's changes to the database 

# executes if error thrown
except mysql.connector.Error as err:
    print("Error-Code:", err.errno)
    print("Error-Message: {}".format(err.msg))
    
    # error code for missing field value: 3665
    # ex of err-msg for missing field value: Missing value for JSON_TABLE column 'ptype'
    if err.errno == 3665:
        error_doc = nlp(err.msg)
        for token in error_doc:
            if token.dep_ == 'pobj':
                if token.text == 'ptype':
                    print('What type of pizza would you like?')
    

# always executes
finally:
    cursor.close()
    cnx.close()
