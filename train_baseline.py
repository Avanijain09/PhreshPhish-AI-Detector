import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

print("Dataset load kar rahe hain...")
df = pd.read_parquet('data/processed/mini_dataset.parquet')

print("Machine Learning ke liye features nikaal rahe hain...")
features = []
labels = []

for index, row in df.iterrows():
    # Compact JSON ko wapas Python dictionary mein badalna
    data = json.loads(row['compact_json'])
    
    # ML model ko sirf numbers chahiye hote hain (text nahi)
    feat = {
        'url_length': data['url_info']['url_length'],
        'num_digits': data['url_info']['num_digits_in_url'],
        'subdomain_depth': data['url_info']['subdomain_depth'],
        'has_password': int(data['flags']['has_password_field']),
        'right_click_disabled': int(data['flags']['right_click_disabled'])
    }
    features.append(feat)
    
    # Label: 1 agar phish hai, 0 agar benign
    labels.append(1 if row['label'] == 'phish' else 0)

X = pd.DataFrame(features)
y = labels

# Data ko Train (80%) aur Test (20%) mein split karna
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nLogistic Regression model train ho raha hai...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Test data par model ko check karna
y_pred = model.predict(X_test)

print("\n=== BASELINE MODEL RESULTS ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred, target_names=['Benign (0)', 'Phish (1)']))