import config
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import fr_core_news_md
from nltk.corpus import stopwords
import plotly.express as px
import plotly.graph_objects as go
##charge spacynlp
nlp = fr_core_news_md.load()
stop_words = list(stopwords.words('french'))+['ctre','tcdicount']



##lemmatize word with spacy#############
def lemma_word(word):
    doc=nlp(word)
    for t in doc:
        token=t.lemma_
    return token
###prerocess#####
def preprocess(row):
    content = row['body']
    tokens = nltk.word_tokenize(content)
    tokens= [w for w in tokens if w.isalpha()]
    tokens= [lemma_word(word) for word in tokens]
    tokens=[word for word in tokens if len(word)>3]
    tokens= [word for word in tokens if not word in stop_words]
    all_words = ( " ".join(tokens))
    #print(tokens)
    return all_words
###############################sentimentmapvalue#######################
#4-5=> Positive 1,  1-2=> Negative(3), 3=> Neutral(2) 
def map_sentiment_value(rating):
    if(int(rating)==3):
        return 2
    elif(int(rating)<3):
        return 3
    else:
        return 1 
######sentimentsmappingstring####
def map_sentiment_string(rating):
    if(int(rating)==3):
        return 'neutre'
    elif(int(rating)<3):
        return 'negatif'
    else:
        return 'positif'  
###############################"LSTM Model######################################




if __name__ == "__main__":
    df_reviews = pd.read_csv(config.TRAINING_FILE)
    df= df_reviews.copy()
    #print(df.head())
    column=['Unnamed: 0']
    df = df.drop(column, axis=1)
    df=df.rename(columns={"date_published": "date"})
    df.date = pd.to_datetime(df.date)
    timezone_name = 'Europe/Paris'
    df.date=df.date.dt.tz_convert(timezone_name)
    df["year"] = df.date.dt.year
    df["month"] = df.date.dt.month
    df['body'] = df['body'].str.lower()
    df['body'] = df['body'].str.replace('[^\w\s]','')
    df['words'] = df.apply(preprocess, axis=1)
    df['sentiment']= df.rating.apply(map_sentiment_string)
    df['sentiment_value']=df.rating.apply(map_sentiment_value)
    df.to_csv('df_preprocess.csv')
    print(df.head())
    print(df.shape)
    #fig = px.pie(df, values='sentiment', title='Population of European continent')
    #fig.show()
    