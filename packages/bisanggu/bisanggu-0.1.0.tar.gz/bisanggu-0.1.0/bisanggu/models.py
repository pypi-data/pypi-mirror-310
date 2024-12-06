import pandas as pd
import xgboost as xgb
import joblib

model_path = '/Users/jungjinho/Desktop/bisanggu/Phishing_model_02.pkl'

def preprocess_data(df):
    columns_to_drop = ['URL', 'IP Address', 'Country', 'User Country', 'Countries Match', 'Creation Date', 'Expiration Date', 'Registrant Name', 'Final URL', 'redirection_count', 'external_domain_requests', 'malicious_file_downloads']
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    bool_columns = ['Is Obfuscated', 'Window Location Redirect', 'SSL Used', 'Cookie Access', 'iframe_present', 'favicon', 'x frame option', 'spf', 'txt', 'lang']
    df[bool_columns] = df[bool_columns].replace({True: 1, False: 0})
    
    nan_columns = ['Hidden Iframe Count', 'Content Size (bytes)', 'Domain Age (days)']
    df[nan_columns] = df[nan_columns].apply(pd.to_numeric, errors='coerce')
    
    return df

def load_model(model_path):
    return joblib.load(model_path)

def predict(features, model):
    dmatrix = xgb.DMatrix(pd.DataFrame([features]))
    return model.predict(dmatrix)
