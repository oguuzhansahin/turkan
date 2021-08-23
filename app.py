import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from credentials import *
from utils import (authentication_api,
                   call_pretrained_model,
                   extract_new,
                   find_question_link,                               
)

app = Flask(__name__)

api, auth = authentication_api(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

tokenizer,model,nlp = call_pretrained_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    
    if request.method =="POST":
        
        prediction_text = ""

        tweet_link = request.form['tweet_link']
        tweet_id = tweet_link.split("/")[-1]
        try:
            tweet_info = api.get_status(tweet_id)
            tweet_info = " ".join(tweet_info.text.split("\n"))
                
            question,link = find_question_link(tweet_info)
            print(question)
            print(link)
        
            news_text = extract_new(link)
        
        except:
            
            print("Haberi alamıyorum abi")
        
        if news_text is not None:
            result = nlp(question = question,
                         context = news_text)
            print(result)
            if result['score'] > 0.1:
                prediction_text = result['answer']
                api.update_status(result['answer'] + " " + tweet_link)
            else:
                
                prediction_text = "Bu soruya cevap bulamadım..."
        else:
            prediction_text = "Bu soruya cevap bulamadım..."
        
        
        #modele sor
        #outputu yazdır


    return render_template('index.html', prediction_text=prediction_text)


if __name__ == "__main__":
    app.run(debug=True)