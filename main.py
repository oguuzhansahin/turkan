import torch
import fasttext
from credentials import * 
from utils import (authentication_api,
                   call_pretrained_model,
                   extract_new,
                   find_tweet_text_and_link,                               
)

api, auth = authentication_api(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tokenizer,model,nlp = call_pretrained_model()
question_classifier = fasttext.load_model("soru_cumlesi_classifier/results/model/sentence.model.bin")


def search_timeline(api,count):
    
    timeline = api.home_timeline(count=count)   
    for tweet in timeline:           
        tweet_link = f" https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            
        try:            
            tweet_text,link = find_tweet_text_and_link(tweet.text)      
            tweet_text = " ".join(tweet_text.split())
            print("Tweet text: ",tweet_text)
            print("Tweet link: ", link)
            
            is_question = question_classifier.predict(tweet_text)[0][0].lstrip("__label__")
            print("Is question? : ",is_question)
            
            if  is_question == "1":
                question = tweet_text
                print("\n\n")              
                print("Soru: ", question)
                print("Link: ", link)
                
                text = extract_new(link)
                
                if text is None:
                    print("\n")
                    print("Haber metni çekilemedi..!")
                    print(30 * "*")
                    print("\n\n")
                    
                else:
                    
                    result = nlp(question = question,
                                 context = text)
                    print(result)
                                   
                    if result['score'] > 0.4:
                        #api.update_status(result['answer'] + " " + tweet_link)
                        print("\n")
                        print("Tweet başarıyla gönderildi...")
                        print(30 * "*")
                        print("\n\n")
                    else:
                        print("\n")
                        print("Skor çok düşük")
                        print(30 * "*")
                        print("\n\n")
            else:
                print("\n")
                print("Bu cevaplanabilecek bir tweet değil...")
                print(30 * "*")
                print("\n\n")
        except:
            print("\n")
            print("Bir hata oluştu")
            print(30 * "*")
            print("\n\n")
            continue

def main():
    
    search_timeline(api, count=10)
    
if __name__=="__main__":
    main()
