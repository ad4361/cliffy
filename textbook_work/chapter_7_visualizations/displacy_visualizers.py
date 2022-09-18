import spacy
from spacy import displacy  # !!! import displacy

nlp = spacy.load('en_core_web_sm')
doc1 = nlp('I want a Greek pizza.')
doc2 = nlp('Microsoft Windows is a family of proprietary operating systems developed and sold by Microsoft. Bill Gates announced Microsoft Windows on November 10, 1983. Microsoft first released Windows for sale on November 20, 1985. Windows 1.0 was initially sold for $100.00, and its sales surpassed 500,000 copies in April 1987. For comparison, more than a million copies of Windows 95 were sold in just the first 4 days.')
doc3 = nlp('I have a relaxed pair of jeans. Now I want a skinny pair.')


# to view each of the different visualizations, after running this code and pointing the browser to
# localhost:5000, enter CTRL + C into the terminal and then refresh the browser. this will allow the
# next displacy.serve() command to run and the new visualization will appear in the browser


# for dependency visualization
displacy.serve(doc1, style='dep')

# for named entity visualization
displacy.serve(doc2, style='ent')

# for sentence-by-sentence dependency visualization
spans = list(doc3.sents)
displacy.serve(spans, style='dep')

