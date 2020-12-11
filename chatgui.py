import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import train_chatbot as train 
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('data.json').read())
books_file = open('books.json').read()
books_data = json.loads(books_file)
books = books_data['books']
words = train.words
classes = train.classes


def search_author(author, dataset):
    books = dataset['books']


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    sugAut=""
    sugBook=""
    if (tag == "SuggestionDeLivre"):
        sugBook = tag
    if (tag == "RechercheAuteur"):
        sugAut = tag
    list_of_intents = intents_json['data']
    result = ""
    for i in list_of_intents:
        if(i['subject'] == sugBook):
            book = random.choice(books)
            result ="Je vous suggère " + book['title'] + "\n"+"Description: \n"+ book['description']+ "\n \n"+ "Il se trouve ici :"+book['website']
            break    
        elif(i['subject'] == sugAut):
            book = random.choice(books)
            result ="Je vous suggère " + book['author'] + " qui a écrit le livre '"+book['title']+"' que vous pourrez trouver ici  :"+book['website']
            break  
        elif(i['subject']== tag):
            result = random.choice(i['outputs'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

p = bow("Bonjour", words,show_details=False)
res = model.predict(np.array([p]))[0]
results = [[i,r] for i,r in enumerate(res) if r>0.25]
print("*************************************************  \n")
while True:
    msg = input("Message \n")
    print("chatbot:  "+chatbot_response(msg))
