import pandas as pd
import xgboost as xgb
import joblib

def preprocess_data(df):
    # 불필요한 열 제거
    columns_to_drop = [
        'URL', 'IP Address', 'Country', 'User Country', 'Countries Match',
        'Creation Date', 'Expiration Date', 'Registrant Name', 'Final URL',
        'redirection_count', 'external_domain_requests', 'malicious_file_downloads'
    ]
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # 불리언 값을 1과 0으로 변환
    bool_columns = [
        'Is Obfuscated', 'Window Location Redirect', 'SSL Used',
        'Cookie Access', 'iframe_present', 'favicon', 'x frame option',
        'spf', 'txt', 'lang'
    ]
    df[bool_columns] = df[bool_columns].replace({True: 1, False: 0})
    
    # NaN 처리 및 데이터 타입 변환
    nan_columns = ['Hidden Iframe Count', 'Content Size (bytes)', 'Domain Age (days)']
    df[nan_columns] = df[nan_columns].apply(pd.to_numeric, errors='coerce')
    
    return df

DEFAULT_MODEL_PATH = "./bisanggu/Phishing_model_02.pkl"

def load_model(model_path=DEFAULT_MODEL_PATH):
    return joblib.load(model_path)

def predict(features, model):
    processed_features = preprocess_data(pd.DataFrame([features]))
    dmatrix = xgb.DMatrix(processed_features)
    return model.predict(dmatrix)
