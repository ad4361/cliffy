
"""
Function used to summarize text in a spaCy Doc object. This method of summarizing calculates word 
frequencies from a text (not including stop words), and uses these frequencies to calculate the 
"most important" sentences in a text in order to build a summary of 30% length compared to the 
original text.
"""

def summarize(doc):

    from string import punctuation
    from spacy.lang.en.stop_words import STOP_WORDS

    # used to calculate the "most important" 3% of text
    from heapq import nlargest

    # before beginning the summarizing process, we will need to calculate the frequency of each token,
    # except for punctuation marks and stop words (such as 'is', 'and', 'the', etc.)
    #       stop words are the most commonly used words in a language 
    stop_words = list(STOP_WORDS)
    punctuation = punctuation + '\n' + '—'

    # calculate word frequences in the doc's text (not counting stop words and punc).
    # the words with the highest frequencies are most likely the "most important" words
    word_frequencies = {}
    for token in doc:
        if token.text.lower() not in stop_words:
            if token.text.lower() not in punctuation:
                if token.text.lower() not in word_frequencies.keys():
                    word_frequencies[token.text.lower()] = 1
                else:
                    word_frequencies[token.text.lower()] += 1
    
    # shows each relevant word and its frequency in the text
    # for key in word_frequencies:
    #    print(key, word_frequencies[key])

    # calculate the max frequency, then divide all frequencies by it
    max_freq = max(word_frequencies.values())
    for key in word_frequencies:
        word_frequencies[key] = word_frequencies[key]/max_freq

    # calculate the "most important" sentences in the doc using the sent's collective frequency value
    sentence_scores = {}
    for sent in doc.sents:
        for token in sent:
            if token.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[token.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[token.text.lower()]
    
    #for key in sentence_scores:
    #    print(key, sentence_scores[key])

    # calculate the 5% of text that has the highest frequency score (and thus the most importance)
    summary_length=int(len(list(doc.sents))*0.03)    # int() ensures a whole number
    
    
    #                      n              iterable        comparison function
    summary_sents_out_of_order = nlargest(summary_length, sentence_scores, key=sentence_scores.get)

    summary = ''
    for sent in sentence_scores:
        if sent in summary_sents_out_of_order:
            print(sent)
            summary += sent.text + ' '
    summary.lstrip()

    return summary
    
"""
import spacy

nlp = spacy.load('en_core_web_sm')

doc = nlp('A renal diet is formulated for cats that are living with chronic kidney disease, or CKD. This is a highly prevalent condition in the feline population and is most common in the aging and older domesticated feline. It has been shown that the lifespan of cats experiencing CKD can be extended by as much as 2 years when receiving therapeutic diets rather than regular maintenance diets. These diets are low in protein, low in phosphorus, have a high energy density, a higher fat content and include omega-3 fatty acids.\
Renal diets with low protein have been adopted by a number of big pet food manufacturers. Although the diet of a healthy cat should be high in protein, at times it is medically necessary for a cat to eat a low protein diet. For cats living with chronic renal disease, low protein diets lower the amount of nitrogenous waste in the body, helping to decrease the strain put on the kidneys. The exact level of protein that is needed for therapeutic CKD diets is unclear.\
Low protein diets can be formulated as a wet or dry food, with the main difference being the moisture content. Unfortunately, low protein diets are not as palatable to cats as diets high in protein.\
Low protein diets should not be fed to cats with the liver condition known as hepatic encephalopathy because severe protein restriction can be detrimental to animals with this condition. Cats with this condition should be fed a diet with high quality protein sources that have adequate amounts of the amino acids taurine and arginine.\
In low protein diets, unless the protein source is a high quality protein such as an animal-based protein, cats (and especially kittens) have been shown to develop retinal degeneration due to a deficiency in taurine, an essential amino acid for cats that is derived from animal protein.\
Low protein diets have been linked to health defects such as lack of growth, decreased food intake, muscle atrophy, hypoalbuminemia, skin alterations, and more. Cats on lower protein diets are more likely to lose weight, and to lose lean body mass.\
Low protein diets that are high in carbohydrates have been found to decrease glucose tolerance in cats. With a decreased glucose tolerance, clinical observations have confirmed that cats consuming large proportions of metabolizable energy, in the form of carbohydrates rather than protein, are more likely to develop hyperglycemia, hyperinsulinemia, insulin resistance, and obesity.\
Restricting phosphorus has been proven to decrease the progression of CKD. This is because phosphorus can be deposited into soft tissues and become mineralized, which can cause kidney damage.\
Formulating these diets with higher amounts of fat is important to make sure the food is palatable in the absence of protein and promote an increased caloric intake. The higher fat content will also spare the use of protein for energy and help decrease stress on the kidneys. Omega-3 fatty acids are included in therapeutic diets because of their anti-inflammatory properties to aid the diseased kidneys.\
')

summarize(doc)
"""