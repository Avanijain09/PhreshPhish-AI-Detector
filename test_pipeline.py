from datasets import load_dataset
from extractor import compact_html
from llm_infer import analyze_page_with_llm
import json

print("Phishing sample load kar rahe hain...")
ds = load_dataset('phreshphish/phreshphish', split='train', streaming=True)
sample = next(iter(ds.filter(lambda x: x['label'] == 'phish')))

print(f"\nTarget URL: {sample['url']}")
print("Data extract ho raha hai...")
compact_data = compact_html(sample['url'], sample['html'])

print("\nLLM ko analysis ke liye bhej rahe hain...")
result = analyze_page_with_llm(compact_data)

print("\n=== FINAL VERDICT ===")
print(json.dumps(result, indent=2))