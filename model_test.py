import pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import punkt
from nltk.corpus.reader import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

category_codes = {
    'A': 0,
    'F': 1,
    'FT': 2,
    'L': 3,
    'LF': 4,
    'MN': 5,
    'O': 6,
    'PE': 7,
    'PO': 8,
    'SC': 9,
    'SE': 10,
    'US': 11,
}

punctuation_signs = list("?:!.,;")
stop_words = list(stopwords.words('english'))

def create_features_from_text(text):
    
    # Dataframe creation
    lemmatized_text_list = []
    df = pd.DataFrame(columns=['Content'])
    df.loc[0] = text
    df['Content_Parsed_1'] = df['Content'].str.replace("\r", " ")
    df['Content_Parsed_1'] = df['Content_Parsed_1'].str.replace("\n", " ")
    df['Content_Parsed_1'] = df['Content_Parsed_1'].str.replace("    ", " ")
    df['Content_Parsed_1'] = df['Content_Parsed_1'].str.replace('"', '')
    df['Content_Parsed_2'] = df['Content_Parsed_1'].str.lower()
    df['Content_Parsed_3'] = df['Content_Parsed_2']
    for punct_sign in punctuation_signs:
        df['Content_Parsed_3'] = df['Content_Parsed_3'].str.replace(punct_sign, '')
    df['Content_Parsed_4'] = df['Content_Parsed_3'].str.replace("'s", "")
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized_list = []
    text = df.loc[0]['Content_Parsed_4']
    text_words = text.split(" ")
    for word in text_words:
        lemmatized_list.append(wordnet_lemmatizer.lemmatize(word, pos="v"))
    lemmatized_text = " ".join(lemmatized_list)    
    lemmatized_text_list.append(lemmatized_text)
    df['Content_Parsed_5'] = lemmatized_text_list
    df['Content_Parsed_6'] = df['Content_Parsed_5']
    for stop_word in stop_words:
        regex_stopword = r"\b" + stop_word + r"\b"
        df['Content_Parsed_6'] = df['Content_Parsed_6'].str.replace(regex_stopword, '')
    df = df['Content_Parsed_6']
    df = df.rename(columns={'Content_Parsed_6': 'Content_Parsed'})
    
    # TF-IDF
    features = tfidf.transform(df).toarray()
    
    return features

def get_category_name(category_id):
    for category, id_ in category_codes.items():    
        if id_ == category_id:
            return category
        
def predict_from_text(text):
    
    # Predict using the input model
    prediction_svc = best_rfc.predict(create_features_from_text(text))[0]
    prediction_svc_proba = best_rfc.predict_proba(create_features_from_text(text))[0]
    
    # Return result
    category_svc = get_category_name(prediction_svc)
    
    print("The predicted category using the Random Forest model is %s." %(category_svc) )
    print("The conditional probability is: %a" %(prediction_svc_proba.max()*100))