import spacy

nlp = spacy.load('en_core_web_lg')
doc = nlp('I want a green apple.')

# calculating semantic similarity of a Doc object and a Span object
print(doc.similarity(doc[2:5]))
# for en_core_web_sm: 0.7725644653859445
# for en_core_web_md: 0.8776482403927138
# either way, we can see that the content of the two containers is similar

print(doc.similarity(doc))
# 1.0: an object is identical in content to itself


# comparing two different docs with different content:
doc2 = nlp('I like red oranges.')
print(doc2.similarity(doc[2:5]))
# for en_core_web_sm: 0.2119930988230391
# for en_core_web_lg: 0.7266315063402384
# note that en_core_web_sm does not include word vectors, meaning similarity results may be inaccurate


# compare two tokens: oranges and apples
token = doc2[3:4][0] # oranges # doc2[3:4] is a Span object, but appending [0] converts it into a token
print(token.similarity(doc[4:5][0]))
# for en_core_web_sm: 0.28983006
# for en_core_web_lg: 0.50937694 