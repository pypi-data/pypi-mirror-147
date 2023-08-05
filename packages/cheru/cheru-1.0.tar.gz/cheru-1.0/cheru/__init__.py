import pandas as pd
import numpy as np
import requests
from textblob import TextBlob as tb
from bs4 import BeautifulSoup as bs
from matplotlib import pyplot as plt
#from wordcloud import WordCloud
import nltk
import re 
from IPython.display import clear_output
import matplotlib.pyplot as plt
import seaborn as sns




def link(url , pg = 50 ,output = "df"):
    if url[12:12+6] == "amazon":
        print("Amazon Link Detected")
        return find_amazon_data_ruku(url , pg,  output )
    else:
        print("FLipkart Link Detected")
        return find_Flip_data_ruku(url , pg , output)
#Amazon Website
def find_amazon_data_ruku(link , pg = 50 , output = "json"):
    raw = link
    last = pg
    code = 0
    review = []
    for p in range(1,last+1):
        num = raw.find("ref")
        url_1 = raw[0:num]
        url_2 = f"ref=cm_cr_arp_d_paging_btm_next_{p}?ie=UTF8&reviewerType=all_reviews&pageNumber={p}"
        finalurl = url_1+url_2
        finalurl = finalurl.replace("/dp/","/product-reviews/")
        data = requests.get(finalurl)
        print("amazon Link Detected")
       
        if (data.reason) == "OK" :
            code = code+1
        data = bs(data.content)
        data = data.find_all(class_= "aok-relative")
        print(int(p/last *100) , "% Completion")
        print(int(code/last * 100) , "% Success Rate")
        clear_output(wait=True)

        for d in data:
            d = {
                "Rating" : float(d.find(class_="a-link-normal").text[0:3]),
                "Title" : d.find(class_="review-title-content").text,
                "Content" : d.find(class_="review-text-content").text
            }
            review.append(d)
    print((code/last) * 100 ,"% is the Sucess rate")
   
    data = pd.DataFrame(review)
    data.replace("\n","",regex=True,inplace=True)

    def mood(t):
        mood = tb(t).sentiment.polarity
        if mood > 0:
            return "Happy"
        elif mood == 0:
            return "No Mood"
        else:
            return "Sad"
    data["Polartiy"] = data["Content"].apply(mood)
    for d in data.columns:
        try:
            data[d] = data[d].apply(low)

        except:
            pass
    if output == "json":
        return review
    else:
        return data

    
    
#flipkart
def find_Flip_data_ruku(link , pg = 50 , output = "json"):
    raw = link
    last = pg
    code = 0
    review = []
    for p in range(1,last+1):
        num = raw.find("&")
        url_1 = raw[0:num+1]+f"page={p}"
        url_1 = url_1.replace("/p/","/product-reviews/")
        
        data = requests.get(url_1)
        
        if (data.reason) == "OK" :
            code = code+1
        data = bs(data.content)
        data = data.find_all(class_= "col _2wzgFH K0kLPL")
        print(int(p/last *100) , "% Completion")
        print(int(code/last * 100) , "% Sucess Rate")
        clear_output(wait=True)

        for d in data:
            d = {
                "Rating" : float(d.find(class_="_1BLPMq").text),
                "Title" : d.find(class_="_2-N8zT").text,
                "Content" : d.find(class_="t-ZTKy").text
            }
            review.append(d)
    print((code/last) * 100 ,"% is the Sucess rate")
   
    data = pd.DataFrame(review)
    data.replace("\n","",regex=True,inplace=True)
    def mood(t):
        mood = tb(t).sentiment.polarity
        if mood > 0:
            return "Happy"
        elif mood == 0:
            return "No Mood"
        else:
            return "Sad"
    data["Polartiy"] = data["Content"].apply(mood)
    for d in data.columns:
        try:
            data[d] = data[d].apply(low)

        except:
            pass
    if output == "json":
        return review
    else:
        return data

    
def show_rating_bar(data):
    try:

        rating = data.groupby(by="Rating")[["Title"]].count()
        sns.barplot(y=rating.Title,x = rating.index)
    except:
        print("Link Error Try with another")
def show_pie_chart(data):
    try:

        x = data.groupby(by="Polartiy")[["Content"]].count()
        plt.figure(figsize=(8,8))
        plt.pie(x = x.Content,autopct='%.2f',explode=[0.2,0,0],shadow=True,labels=x.index);
    except:
        print("Link Error Try with another")
    
def show_Happy_chart(data, n = 1):
    try:
        sad_data = data[data["Polartiy"] == "happy"]
        stopwords = nltk.corpus.stopwords.words("english")
        words = []
        for i in range(0,len(sad_data)):
            a = data.Content[i]
            a = re.sub("[', ),:,(,.,!,&,]"," ",a)
            a = re.sub("[0-9]"," ",a)
            a = " ".join(a.split())
            a = nltk.word_tokenize(a)
            a = nltk.ngrams(a,n)
            for m in a:
                if m not in stopwords:
                    words.append(m)
        val =  nltk.FreqDist(words).values()
        key =  nltk.FreqDist(words).keys()
        data_1 = pd.DataFrame(data={"Key":key, "val": val})
        data_1= data_1.sort_values(by = "val",ascending=False)[0:10]
        plt.figure(figsize=(8,8))
        sns.barplot(x = data_1.val, y = data_1.Key,orient="h")
    except:
        print("Link Error Try with another")
    
def show_Sad_chart(data , n = 1):
    try:
        sad_data = data[data["Polartiy"] == "sad"]
        stopwords = nltk.corpus.stopwords.words("english")
        words = []
        for i in range(0,len(sad_data)):
            a = data.Content[i]
            a = re.sub("[', ),:,(,.,!,&,]"," ",a)
            a = re.sub("[0-9]"," ",a)
            a = " ".join(a.split())
            a = nltk.word_tokenize(a)

            a = nltk.ngrams(a,n)
            for m in a:
                if m not in stopwords:
                    words.append(m)
        val =  nltk.FreqDist(words).values()
        key =  nltk.FreqDist(words).keys()
        data_1 = pd.DataFrame(data={"Key":key, "val": val})
        data_1= data_1.sort_values(by = "val",ascending=False)[0:10]
        plt.figure(figsize=(8,8))
        sns.barplot(x = data_1.val, y = data_1.Key,orient="h")
    except:
        print("Link Error Try with another")
    
def low(text):
    return text.lower()
    
    