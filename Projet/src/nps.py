########NET PROMOTER SCORE
# 
#https://www.definitions-marketing.com/definition/net-promoter-score/
# Théoriquement, le Net Promoter Score peut varier de –100 (100% de détracteurs) à +100 (100% de promoteurs).
#Un NPS de 0 indique une satisfaction “neutre” des participants,
#Plus le NPS est positif, meilleur il est.
#Un Net Promoter Score de 50 est considéré comme excellent et difficile à atteindre.
#
# 
# 
# 
# ######

import config
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
import fr_core_news_md
nlp = fr_core_news_md.load()
from matplotlib import pyplot as plt
stop_words = list(stopwords.words('french'))+['ctre','tcdicount']
##nombre de detracteurs
def nombre_de_detrateurs(df):
    return int(df.detracteurs[df['detracteurs']==1].count())


######nombre de passifs#########
def nombre_de_passifs(df):
    return int(df.passifs[df['passifs']==1].count())
######nombre de promoteurs####
def nombre_de_promoteurs(df):
    return int(df.promoteurs[df['promoteurs']==1].count())
###nps score###
def nsp_score(df):
    #nombre de repondants
    total= df.shape[0]
    total_promoteurs=nombre_de_promoteurs(df)
    total_detracteurs=nombre_de_detrateurs(df)
    return ((total_promoteurs * 100) / total) - ((total_detracteurs * 100) / total)


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
    

############Ngrams ANalysis##########################################
    #################Unigrams#####################
def unigrams(descriptions, n=None):
    vec = CountVectorizer(ngram_range = (1,1), max_features = 20000).fit(descriptions)
    bag_of_words = vec.transform(descriptions)
    sum_words = bag_of_words.sum(axis = 0) 
    words_freq = [(word, sum_words[0, i]) for word, i in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse = True)
    return words_freq[:n]
    
       
    ##################bigrams ####################
def bigrams(descriptions, n=None):
    vec = CountVectorizer(ngram_range = (2,2), max_features = 30000).fit(descriptions)
    bag_of_words = vec.transform(descriptions)
    sum_words = bag_of_words.sum(axis = 0) 
    words_freq = [(word, sum_words[0, i]) for word, i in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse = True)
   
    return words_freq[:n]
    ###################trigrams#####################
def trigrams(descriptions, n=None):
    
    vec = CountVectorizer(ngram_range = (3,3), max_features = 20000).fit(descriptions)
    bag_of_words = vec.transform(descriptions)
    sum_words = bag_of_words.sum(axis = 0) 
    words_freq = [(word, sum_words[0, i]) for word, i in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse = True)
   
    return words_freq[:n]



if __name__ == "__main__":
    df = pd.read_csv(config.TRAINING_FILE)
    
    print(df.head())
    print(df.shape)
    column=['Unnamed: 0']
    df = df.drop(column, axis=1)
    df['detracteurs'] = np.where(df['rating'] < 4, 1, 0)
    df['passifs'] = np.where(df['rating'] == 4, 1, 0)
    df['promoteurs'] = np.where(df['rating'] == 5, 1, 0)
    #print(df.head())
    df['body'] = df['body'].str.lower()
    df['body'] = df['body'].str.replace('[^\w\s]','')
    df = df[[ 'body', 'detracteurs', 'passifs', 'promoteurs']]
    df_detracteurs = df[df['detracteurs']==1]
    df_passifs= df[df['passifs']==1]
    df_promoteurs = df[df['promoteurs']==1]
    ####################BIGRAMS######################################
                ####promoteurs bigram#####
    promoteur_bigrams = bigrams(df_promoteurs['body'], n=25)
    promoteur_bigrams_df = pd.DataFrame(promoteur_bigrams)
    promoteur_bigrams_df.columns=["bigrams", "frequence"]
    promoteur_bigrams_df.to_csv('fre_bigram_pro.csv')
                #####passifs bigrams####
    passif_bigrams = bigrams(df_passifs['body'], n=25)
    passif_bigrams_df = pd.DataFrame(passif_bigrams)
    passif_bigrams_df.columns=["bigrams", "frequence"]
    passif_bigrams_df.to_csv('fre_bigram_passifs.csv')
                ####detracteurs#########
    detracteurs_bigrams = bigrams(df_detracteurs['body'], n=25)
    detracteurs_bigrams_df = pd.DataFrame(detracteurs_bigrams)
    detracteurs_bigrams_df.columns=["bigrams", "frequence"]
    detracteurs_bigrams_df.to_csv('fre_bigram_detracteur.csv')
    ################TRIGRAMS###########################
                ####promoteurs triigram#####
    promoteur_trigrams = trigrams(df_promoteurs['body'], n=25)
    promoteur_trigrams_df = pd.DataFrame(promoteur_trigrams)
    promoteur_trigrams_df.columns=["trigrams", "frequence"]
    promoteur_trigrams_df.to_csv('fre_trigrams_pro.csv')
                #####passifs bigrams#######
    passif_trigrams = trigrams(df_passifs['body'], n=25)
    passif_trigrams_df = pd.DataFrame(passif_trigrams)
    passif_trigrams_df.columns=["trigrams", "frequence"]
    passif_trigrams_df.to_csv('fre_trigrams_passifs.csv')
                ####detracteurs#########
    detracteurs_trigrams = trigrams(df_detracteurs['body'], n=25)
    detracteurs_trigrams_df = pd.DataFrame(detracteurs_trigrams)
    detracteurs_trigrams_df.columns=["trigrams", "frequence"]
    detracteurs_trigrams_df.to_csv('fre_trigrams_detracteur.csv')


    df['text_pre'] = df.apply(preprocess, axis=1)
    df = df[[ 'text_pre', 'detracteurs', 'passifs', 'promoteurs']]
    df_detracteurs = df[df['detracteurs']==1]
    df_passifs= df[df['passifs']==1]
    df_promoteurs = df[df['promoteurs']==1]
    
    #############Unigrams#################################
                ####promoteurs unigram#####
    promoteur_unigrams = unigrams(df_promoteurs['text_pre'], n=25)
    promoteur_unigrams_df = pd.DataFrame(promoteur_unigrams)
    promoteur_unigrams_df.columns=["unigrams", "Promoteurs"]
    promoteur_unigrams_df.to_csv('fre_unigrams_pro.csv')
                #####passifs unigrams#######
    passif_unigrams = unigrams(df_passifs['text_pre'], n=25)
    passif_unigrams_df = pd.DataFrame(passif_unigrams)
    passif_unigrams_df.columns=["unigrams", "Passifs"]
    passif_unigrams_df.to_csv('fre_unigrams_passifs.csv')
                ####detracteurs#########
    detracteurs_unigrams = unigrams(df_detracteurs['text_pre'], n=25)
    detracteurs_unigrams_df = pd.DataFrame(detracteurs_unigrams)
    detracteurs_unigrams_df.columns=["unigrams", "Detracteur"]
    detracteurs_unigrams_df.to_csv('fre_unigrams_detracteur.csv')
    #########Concatenation###########################################
    unigrams_final = pd.concat([promoteur_unigrams_df['unigrams'], 
                         passif_unigrams_df['unigrams'],
                         detracteurs_unigrams_df['unigrams']],
                         ignore_index=True, 
                         sort=False)
    
    unigrams_final = unigrams_final.drop_duplicates().reset_index(drop=True).to_frame()
    unigrams_final = unigrams_final.merge(promoteur_unigrams_df, on='unigrams', how='left')
    unigrams_final = unigrams_final.merge(passif_unigrams_df, on='unigrams', how='left')
    unigrams_final = unigrams_final.merge(detracteurs_unigrams_df, on='unigrams', how='left')
    unigrams_final = unigrams_final.fillna(0)
    unigrams_final.to_csv('final_unigram.csv')

    
    
   