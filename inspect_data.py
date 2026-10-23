from datasets import load_dataset

print("PhreshPhish dataset stream ho raha hai...")

# streaming=True se 36 GB download nahi hoga, direct live sample aayega
dataset = load_dataset("phreshphish/phreshphish", split="train", streaming=True)

for i, sample in enumerate(dataset.take(3)):
    print(f"\n{'='*50}")
    print(f"Sample #{i+1}")
    print(f"URL: {sample.get('url')}")
    print(f"Label: {sample.get('label')} (1 = Phish, 0 = Benign)")
    print(f"Target Brand: {sample.get('target')}")
    print(f"Language: {sample.get('lang')}")
    html_snippet = sample.get('html', '')[:300]
    print(f"HTML Snippet (first 300 chars):\n{html_snippet}...")
    print(f"{'='*50}")