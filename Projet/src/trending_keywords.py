import config
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import pickle
import itertools
import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
#import fr_core_news_md
#nlp = fr_core_news_md.load()
from matplotlib import pyplot as plt
stop_words = list(stopwords.words('french'))+['ctre','tcdicount']



def max_sum_sim(doc_embedding, candidate_embeddings, candidates, top_n, nr_candidates):
    # Calculate distances and extract keywords
    distances = cosine_similarity(doc_embedding, candidate_embeddings)
    distances_candidates = cosine_similarity(candidate_embeddings, 
                                            candidate_embeddings)

    # Get top_n words as candidates based on cosine similarity
    words_idx = list(distances.argsort()[0][-nr_candidates:])
    words_vals = [candidates[index] for index in words_idx]
    distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

    # Calculate the combination of words that are the least similar to each other
    min_sim = np.inf
    candidate = None
    for combination in itertools.combinations(range(len(words_idx)), top_n):
        sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
        if sim < min_sim:
            candidate = combination
            min_sim = sim

    return [words_vals[idx] for idx in candidate]

############Extraction##################""""
# Diversify the keywords using max sum similarity, higher the value of nr_candidates higher the diversity
def extract_keywords_bert_diverse(doc,top_n=150,nr_candidates=300):
    n_gram_range = (1,1)
    # Extract candidate words/phrases using count vectorizer (TF-IDF Scores)
    count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([doc])
    candidates = count.get_feature_names()
    # Embeddings of the document using Bert    
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    doc_embedding = model.encode([doc])
    candidate_embeddings = model.encode(candidates)
    keywords=max_sum_sim(doc_embedding, candidate_embeddings, candidates, top_n, nr_candidates)
    return keywords
################################get_trending_keywords###################
def get_trending_keywords(pos_data,neg_data,num_keywords):
    keywords={}
    limit=list(pos_data[-1000::])
    corpus=' '.join(map(str, limit))
    print(type(corpus))
    keywords['positive']=extract_keywords_bert_diverse(corpus,num_keywords)
    limit=list(neg_data[-200::])
    corpus=' '.join(map(str, limit))
    keywords['negative']=extract_keywords_bert_diverse(corpus,num_keywords)
    return keywords










if __name__ == "__main__":
    df_final = pd.read_csv(config.FINAL)
    df=df_final.copy()
    df_pos = df[df['sentiment']=='positif']['words']
    a=df_pos[-250::]
    df_neg=df[df['sentiment']=='negatif']['words']
    trending=get_trending_keywords(df_pos, df_neg,200)
    print(trending)
    to_pic = open("data.pkl", "wb")
    pickle.dump(trending, to_pic)
    to_pic.close()
