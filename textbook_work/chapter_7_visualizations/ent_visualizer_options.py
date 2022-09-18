from click import option
import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_md')
doc = nlp('In 2011, Google launched Google +, its fourth foray into social networking.')

# set title for doc, which is displayed in the entity visualization
doc.user_data['title'] = "An example of an entity visualization, using options"

# ents: the only types of named entities that will be highlighted
# color: the colors assigned to entity types (this is done by default but you can customize colors) 
options = {'ents': ['ORG', 'PRODUCT', 'DATE'], 
'colors': {'ORG': 'aqua', 'PRODUCT': 'aqua', 'DATE': 'yellow'} }

displacy.serve(doc, style='ent', options=options)

