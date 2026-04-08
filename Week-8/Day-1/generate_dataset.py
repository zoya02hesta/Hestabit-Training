import json
import random
import os

os.makedirs("data", exist_ok=True)

QA_QUESTIONS = [
    ("What is Python?", "Python is a high-level programming language used for web development, AI, and automation."),
    ("What is a variable?", "A variable is a container for storing data values."),
    ("What is an API?", "An API is a way for applications to communicate with each other."),
]

REASONING_QUESTIONS = [
    ("If a car travels 100 km in 2 hours, what is the speed?", "Speed = Distance / Time = 100 / 2 = 50 km/h."),
    ("If 5 workers build a wall in 10 days, how many days for 10 workers?", "More workers reduce time. Answer: 5 days."),
]

EXTRACTION_INPUTS = [
    ("Name: Zoya Fatima, Age: 22, Role: ML Intern",
     {"name": "Zoya Fatima", "age": 22, "role": "ML Intern"}),
]

def generate_sample():
    choice = random.choice(["qa", "reasoning", "extraction"])

    if choice == "qa":
        q, a = random.choice(QA_QUESTIONS)
        return {
            "instruction": "Answer the question",
            "input": q,
            "output": a
        }

    elif choice == "reasoning":
        q, a = random.choice(REASONING_QUESTIONS)
        return {
            "instruction": "Solve step by step",
            "input": q,
            "output": a
        }

    else:
        inp, out = random.choice(EXTRACTION_INPUTS)
        return {
            "instruction": "Extract structured information",
            "input": inp,
            "output": json.dumps(out)
        }

def main():
    with open("data/raw.jsonl", "w") as f:
        for _ in range(1200):  # >1000 samples
            json.dump(generate_sample(), f)
            f.write("\n")

    print("✅ Dataset generated: data/raw.jsonl")

if __name__ == "__main__":
    main()