import spacy
nlp = spacy.load('en_core_web_sm')

# to find the specific statistical model you're using:
# print(nlp.meta['lang'] + '_' + nlp.meta['name'])
# en_core_web_sm

from spacy import util
print(util.get_package_path('en_core_web_sm'))

# to find the path to the model package, you need to use the above path with one more folder appended:
print(nlp.meta['lang'] + '_' + nlp.meta['name'] + '-' + nlp.meta['version'])

# to find your default pipeline components associated with nlp:
# print(nlp.pipe_names)



# performing spacy.load() MANUALLY:

lang = 'en'
pipeline = ['tagger', 'parser', 'ner']
# this path below is obtained from the print statements before
model_data_path = '/Users/adrie/AppData/Local/Programs/Python/Python38/lib/site-packages/en_core_web_sm/en_core_web_sm-2.3.1'
lang_cls = spacy.util.get_lang_class(lang)  #obtain the Language class
nlp = lang_cls()

for name in pipeline:
    component = nlp.create_pipe(name)
    nlp.add_pipe(component)
nlp.from_disk(model_data_path)
# note that pipeline components can't be used until the language data is loaded from the disk


# testing that the manual loading of the statistical model worked
doc = nlp('Hello')
print(doc[0])

