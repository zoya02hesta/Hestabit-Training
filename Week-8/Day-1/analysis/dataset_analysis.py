import json
import matplotlib.pyplot as plt
from collections import Counter  # ✅ add here

def load_data(path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f]

def get_lengths(data):
    lengths = []
    for item in data:
        text = f"{item['instruction']} {item['input']} {item['output']}"
        lengths.append(len(text.split()))
    return lengths

def main():
    data = load_data("data/train.jsonl")

    if not data:
        print("❌ No data found. Run generator first.")
        return

    # ✅ ADD THIS HERE
    tasks = [item["instruction"] for item in data]
    print("📊 Task distribution:")
    print(Counter(tasks))

    lengths = get_lengths(data)

    print(f"📊 Total samples: {len(data)}")
    print(f"📈 Max length: {max(lengths)}")
    print(f"📉 Min length: {min(lengths)}")
    print(f"📊 Avg length: {sum(lengths)/len(lengths)}")

    plt.hist(lengths, bins=30)
    plt.xlabel("Token Length")
    plt.ylabel("Frequency")
    plt.title("Token Length Distribution")

    plt.savefig("analysis/token_distribution.png")
    print("📊 Plot saved at analysis/token_distribution.png")

if __name__ == "__main__":
    main()