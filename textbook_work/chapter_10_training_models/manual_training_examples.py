import spacy

nlp = spacy.load('en_core_web_sm')

# imagine you have the following utterances:
# Could you send a taxi to Solnce?
# Is there a flat rate to the airport from Solnce?
# How long is the wait for a taxi right now?

# turn the above into training examples manually (in another python file we will automate this process)
# list of three tuples
train_exams = [
    ('Could you send a taxi to Solnce?', 
    {'entities': [(25, 31, 'GPE')]}),
    #           start  end  label

    ('Is there a flat rate to the airport from Solnce?', 
    {'entities': [(41, 47, 'GPE')]}),

    ('How long is the wait for a taxi right now?', 
    {'entities': []})
]