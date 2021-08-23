import tweepy
import re
from credentials import MODEL_NAME,FOOLISH
from newspaper import Article

from transformers import (
    AutoTokenizer, 
    AutoModelForQuestionAnswering, 
    pipeline
)

def authentication_api(API_KEY, 
                       API_SECRET_KEY,
                       ACCESS_TOKEN,
                       ACCESS_TOKEN_SECRET):

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    
    return api,auth


def call_pretrained_model(model_name = MODEL_NAME):
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    nlp=pipeline("question-answering", model=model, tokenizer=tokenizer)
    
    return tokenizer,model,nlp


def extract_new(url):
    
    article = Article(url)
    article.download()
    article.parse()
    text = article.text
    text = " ".join(text.split())
    
    if text == FOOLISH or text == "":
        return None
    
    return text


def find_tweet_text_and_link(tweet):
    
    match = re.search(r'(https?://\S+)', tweet)
    tweet_text, link = tweet[:match.span()[0]],tweet[match.span()[0]:match.span()[1]]
    
    return tweet_text,link

