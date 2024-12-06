from bisanggu.analyzer import crawl_website
from bisanggu.models import load_model, predict

# 모델 경로
model_path = "/Users/jungjinho/Desktop/bisanggu/Phishing_model_02.pkl"

# 머신러닝 모델 로드
model = load_model(model_path)  # 명시적으로 경로 전달

# URL 분석
headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://replyn176.wixstudio.com/my-site"
result = crawl_website(url, headers)

# 예측 수행
if result:
    prediction = predict(result, model)
    print(f"Prediction: {'Phishing' if prediction[0] > 0.5 else 'Safe'}")
else:
    print("Failed to analyze the URL.")