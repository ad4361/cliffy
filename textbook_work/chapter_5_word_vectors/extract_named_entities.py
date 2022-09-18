import spacy
nlp = spacy.load('en_core_web_md')

# first sample text
doc1 = nlp('Google Search, often referred to as simply Google, is the most used search engine nowadays. It handles a huge number of searches each day.')

# second sample text
doc2 = nlp('Microsoft Windows is a family of proprietary operating systems developed and sold by Microsoft. The company also produces a wide range of other software for desktops and servers.')

# third sample text
doc3 = nlp('Titicaca is a large, deep mountain lake in the Andes. It is known as the highest navigable lake in the world.')

docs = [doc1, doc2, doc3]
spans = {}

for j, doc in enumerate(docs):
    named_entity_span = [doc[i].text for i in range(len(doc)) if doc[i].ent_type != 0]
    print(named_entity_span)
    named_entity_span = ' '.join(named_entity_span)
    named_entity_span = nlp(named_entity_span)
    spans.update({j:named_entity_span})

print('\ndoc1 is similar to doc2: ' + str(spans[0].similarity(spans[1])) + '\n')
print('doc1 is similar to doc3: ' + str(spans[0].similarity(spans[2])) + '\n')
print('doc2 is similar to doc3: ' + str(spans[1].similarity(spans[2])) + '\n')


# IN THEORY this should work, but for some reason the ner is recognizing normal nouns (such as "each",
# "day", "lake", and "mountain") as named entities, which is throwing off calculations. the above print
# statements should show that doc1 and doc2 are the most similar, since Google and Microsoft are often
# found together in the same text than Google and Andes or Microsoft and Titicaca

