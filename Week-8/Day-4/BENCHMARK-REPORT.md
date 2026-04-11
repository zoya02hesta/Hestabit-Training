# 📊 LLM Inference Benchmark Report

## 🧠 Overview

This project evaluates and optimizes inference performance of a Large Language Model (LLM) across different precision modes and configurations. The goal is to understand trade-offs between **speed**, **memory usage**, and **output quality**.

The benchmarking was conducted on a GPU-enabled environment using multiple inference strategies including full precision and quantized models.

---

## ⚙️ Experimental Setup

* **Model**: TinyLlama (Fine-tuned + Base variants)
* **Hardware**: NVIDIA Tesla T4 (15GB VRAM)
* **Framework**: Hugging Face Transformers + PyTorch
* **Precision Modes Tested**:

  * FP16 (Half Precision)
  * INT8 Quantization (bitsandbytes)
  * INT4 Quantization (bitsandbytes)

---

## 🧪 Benchmark Methodology

Each model configuration was evaluated using a set of prompts:

* "Explain quantization in simple terms"
* "What is LoRA in AI?"
* "Write Python code for Fibonacci"

### Metrics Collected:

* ✅ Tokens per second (Throughput)
* ✅ Latency (Time to generate output)
* ✅ VRAM Usage (GPU memory consumption)
* ✅ Qualitative Accuracy (manual observation)

---

## 📈 Results Summary

| Mode | Avg Tokens/sec ⚡ | Avg Latency ⏱️ | VRAM Usage 📉 |
| ---- | ---------------- | -------------- | ------------- |
| FP16 | ~32              | ~3.0s          | ~2.25 GB      |
| INT8 | ~9               | ~10.9s         | ~2.23 GB      |
| INT4 | ~22              | ~4.5s          | ~2.28 GB      |

---

## 🔍 Detailed Observations

### 🚀 FP16 (Half Precision)

* Delivered the **highest throughput**
* Lowest latency among all configurations
* Fully utilizes GPU capabilities
* Ideal for production when memory is not a constraint

---

### ❌ INT8 Quantization

* Significantly **slower than expected**
* Minimal VRAM reduction compared to FP16
* Likely affected by:

  * Quantization overhead
  * Suboptimal GPU kernel utilization
* Not recommended in this setup

---

### ⚖️ INT4 Quantization

* Strong balance between **speed and efficiency**
* Much faster than INT8
* Slightly slower than FP16 but still performant
* Best candidate for **resource-constrained deployment**

---

## ⚡ Advanced Features Implemented

### 🔹 Batch Inference

* Multiple prompts processed simultaneously
* Reduced overall latency per request

### 🔹 Streaming Output

* Tokens generated in real-time
* Improves user experience for long responses

### 🔹 Multi-Prompt Benchmarking

* Consistent evaluation across different tasks
* Ensures robustness of results

---

## 🧠 Key Insights

1. **Quantization does not always guarantee speed improvement**

   * INT8 performed worse due to overhead

2. **Memory savings were minimal across configurations**

   * Suggests model size was already manageable

3. **FP16 remains the most optimized path on T4 GPUs**

   * Best hardware compatibility

4. **INT4 provides best trade-off**

   * Reduced compute cost with acceptable performance

---

## ⚠️ Limitations

* Accuracy was evaluated qualitatively (not numerically scored)
* Limited prompt diversity
* Single GPU type (T4) used for testing

---

## 🔮 Future Improvements

* Add quantitative accuracy metrics (BLEU / ROUGE / perplexity)
* Test with larger models (7B, 13B)
* Integrate **vLLM** for optimized serving
* Compare with **llama.cpp (GGUF models)**
* Implement **speculative decoding**

---

## 📁 Project Structure

```
llm-inference-benchmark/
│
├── inference/
│   └── test_inference.py
│
├── benchmarks/
│   ├── results.csv
│   └── BENCHMARK-REPORT.md
│
└── README.md
```

---

## 🏁 Conclusion

This benchmark highlights the importance of **real-world testing over assumptions**.

* FP16 is the fastest and most reliable
* INT8 may not always be beneficial
* INT4 is a strong alternative for efficient deployment

The project successfully demonstrates how to evaluate and optimize LLM inference across multiple configurations in a practical GPU environment.

---

## 🙌 Final Note

This work reflects a hands-on understanding of:

* LLM inference optimization
* Quantization techniques
* Performance benchmarking

It serves as a strong foundation for building scalable and efficient AI systems.

---
