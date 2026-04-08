import json
import os

os.makedirs("data", exist_ok=True)

MAX_TOKENS = 256

def load_data(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return data

def estimate_tokens(text):
    return len(text.split())

def clean_data(data):
    cleaned = []

    for item in data:
        combined = f"{item['instruction']} {item['input']} {item['output']}"

        if not item["instruction"] or not item["output"]:
            continue

        if estimate_tokens(combined) > MAX_TOKENS:
            continue

        cleaned.append(item)

    return cleaned

def split_data(data, train_ratio=0.9):
    import random
    random.shuffle(data)

    split = int(len(data) * train_ratio)
    return data[:split], data[split:]

def save_jsonl(data, path):
    with open(path, "w") as f:
        for item in data:
            json.dump(item, f)
            f.write("\n")

def main():
    data = load_data("data/raw.jsonl")

    print(f"📦 Raw samples: {len(data)}")

    cleaned = clean_data(data)

    print(f"🧹 Cleaned samples: {len(cleaned)}")

    train, val = split_data(cleaned)

    save_jsonl(train, "data/train.jsonl")
    save_jsonl(val, "data/val.jsonl")

    print("✅ Saved train & validation datasets")

if __name__ == "__main__":
    main()