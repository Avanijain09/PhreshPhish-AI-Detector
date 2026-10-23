from datasets import load_dataset
from extractor import compact_html
import pandas as pd
import json
import os

print("Dataset stream ho raha hai...")
ds = load_dataset('phreshphish/phreshphish', split='train', streaming=True)

processed_data = []
phish_count = 0
benign_count = 0
MAX_SAMPLES = 50 # 50 Phish, 50 Benign = Total 100

print("Data extract karna shuru kar rahe hain. Isme 1-2 minute lag sakte hain...")

for sample in ds:
    label = sample['label']
    
    if label == 'phish' and phish_count < MAX_SAMPLES:
        compact_data = compact_html(sample['url'], sample.get('html', ''))
        processed_data.append({
            'url': sample['url'],
            'label': label,
            'target_brand': sample.get('target'),
            'compact_json': json.dumps(compact_data) # LLM ko dene ke liye ready text
        })
        phish_count += 1
        print(f"Phish extract hua: {phish_count}/{MAX_SAMPLES}", end='\r')
        
    elif label == 'benign' and benign_count < MAX_SAMPLES:
        compact_data = compact_html(sample['url'], sample.get('html', ''))
        processed_data.append({
            'url': sample['url'],
            'label': label,
            'target_brand': sample.get('target'),
            'compact_json': json.dumps(compact_data)
        })
        benign_count += 1
        print(f"Benign extract hua: {benign_count}/{MAX_SAMPLES}", end='\r')
        
    if phish_count >= MAX_SAMPLES and benign_count >= MAX_SAMPLES:
        break

print("\n\nExtraction poora hua! Data save kar rahe hain...")

# DataFrame bana kar parquet mein save karna
df = pd.DataFrame(processed_data)

# 'data' folder banayein agar nahi hai
os.makedirs('data/processed', exist_ok=True)

save_path = 'data/processed/mini_dataset.parquet'
df.to_parquet(save_path, engine='pyarrow')

print(f"Dataset successfully save ho gaya yahan: {save_path}")
print(f"Total Rows: {len(df)}")