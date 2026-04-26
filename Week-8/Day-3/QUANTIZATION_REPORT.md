# 📊 Quantisation Report

## 🧾 Overview

This report presents the results of quantising a fine-tuned LLM from FP16 to INT8, INT4, and GGUF formats. The goal was to reduce model size and improve inference efficiency while maintaining acceptable output quality.

---

## 📦 Models Compared

| Format      | Size (GB) | Speed (sec)   | Quality         |
| ----------- | --------- | ------------- | --------------- |
| FP16        | 2.05      | Slow          | High            |
| INT8        | 1.15      | 6.06          | Slight drop     |
| INT4        | 0.71      | Faster        | Moderate drop   |
| GGUF (q8_0) | ~1.15*    | Fastest (CPU) | Slight–Moderate |

*GGUF size is approximately similar to INT8 depending on quantisation type.

---

## 🧠 Observations

* **FP16** provides the highest quality outputs but consumes the most memory.
* **INT8** reduces model size by ~44% with minimal quality degradation and reasonable speed improvement.
* **INT4** achieves ~65% size reduction, making it highly efficient, but with noticeable quality trade-offs.
* **GGUF** format enables efficient CPU-based inference using `llama.cpp`, making it ideal for deployment without GPUs.

---

## ⚖️ Trade-offs

* Reducing precision → decreases memory usage and increases speed
* However, lower precision → reduces output quality
* Choosing the right format depends on deployment constraints:

  * **High accuracy needed** → FP16 / INT8
  * **Low-resource environments** → INT4 / GGUF

---

## 🚀 Performance Summary

* Size reduced from **2.05 GB → 0.71 GB (~65% reduction)**
* INT8 inference time: **~6.06 seconds**
* Significant improvement in deployability across resource-constrained systems

---

## 🏁 Conclusion

Quantisation is a critical step in making large language models production-ready.

* **INT8** offers the best balance between performance and efficiency
* **INT4** is optimal for extreme compression scenarios
* **GGUF** enables seamless CPU deployment using lightweight runtimes

This pipeline demonstrates how LLMs can be optimized for real-world applications without requiring high-end hardware.

---

## 📌 Key Takeaway

Efficient LLM deployment is not just about training —
it's about **optimizing size, speed, and usability** through techniques like quantisation.
