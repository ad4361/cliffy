import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')

# use Matcher constructor with vocab object to create a Matcher instance
matcher = Matcher(nlp.vocab)
pattern = [{"DEP": "nsubj"}, {"DEP": "aux"}, {"DEP": "ROOT"}]
# add pattern to our Matcher instance
matcher.add("NsubjAuxRoot", None, pattern)

doc = nlp('We can overtake them.')

# apply Matcher to sample text and obtain matching tokens in a list
matches = matcher(doc)

# print(matches) : for sample text, prints [(10599197345289971701, 0, 3)]
#                                               match_id        start end

print('Pattern: nsubj + aux + ROOT')

for match_id, start, end in matches:
    span = doc[start:end]
    print('Span matching pattern: ' + span.text)
    print('The positions in the doc matching the pattern are: ' + str(start) + ' - ' + str(end))

