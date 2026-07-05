# cty-small-chatbot-models

Official deep learning model weight repository for [cty-llm-chatbot](https://github.com/CraftThingy-Digital-Innovation/cty-llm-chatbot) local client/server chatbot.

[Bahasa Indonesia](#bahasa-indonesia) | [English](#english)

---

## Bahasa Indonesia

Repositori ini berfungsi sebagai pusat penyimpanan (*hosting*) mandiri untuk berkas-berkas model kecerdasan buatan local chatbot (Llama 3.2, Qwen 2.5, SmolLM2, dan MiniCPM5) yang telah dikonversi ke format **ONNX**, format teroptimasi **ORT** (FlatBuffers), atau format **GGUF** untuk server lokal.

Seluruh aset model biner di repositori ini didistribusikan secara aman menggunakan **Git Large File Storage (LFS)** dan kompatibel 100% dengan pustaka **cty-llm-chatbot**.

### 1. Struktur Folder
Aset model ini diorganisasikan ke dalam direktori berdasarkan keluarga model:
*   `llama/`: Berisi model-model Llama (seperti Llama-3.2-1B-Instruct).
*   `qwen/`: Berisi model-model Qwen (seperti Qwen2.5-1.5B-Instruct atau DeepSeek-R1 Qwen Distill).
*   `smollm/`: Berisi model-model SmolLM (seperti SmolLM2-135M-Instruct).
*   `minicpm/`: Berisi model-model MiniCPM (seperti MiniCPM5-1B-GGUF).
*   `gemma/`: Berisi model-model Gemma (seperti Gemma-2-2B-it).
*   `phi/`: Berisi model-model Phi (seperti Phi-3.5-mini-instruct).

### 2. Opsi Kinerja ORT (FlatBuffers Serialization)
Berkas berakhiran `.ort` adalah model teroptimasi FlatBuffers untuk browser:
*   **Pemuatan Lebih Cepat**: Model ORT dimuat 3x hingga 5x lebih cepat di browser dengan konsumsi memori awal yang jauh lebih rendah.

---

## English

This repository serves as a self-hosted storage hub for local chatbot neural network weights (Llama 3.2, Qwen 2.5, SmolLM2, and MiniCPM5 variants) converted into standard **ONNX** formats, optimized **ORT** (FlatBuffers serialized) graphs, or **GGUF** formats for local endpoints.

All binary weights are stored and tracked using **Git Large File Storage (LFS)** and are 100% compatible with the **cty-llm-chatbot** library.

### 1. Folder Structure
Models are organized in subdirectories based on model families:
*   `llama/`: Contains Llama model checkpoints (e.g. Llama-3.2-1B-Instruct).
*   `qwen/`: Contains Qwen model checkpoints (e.g. Qwen2.5-1.5B-Instruct or DeepSeek-R1 Qwen Distill).
*   `smollm/`: Contains SmolLM model checkpoints (e.g. SmolLM2-135M-Instruct).
*   `minicpm/`: Contains MiniCPM model checkpoints (e.g. MiniCPM5-1B-GGUF).
*   `gemma/`: Contains Gemma model checkpoints (e.g. Gemma-2-2B-it).
*   `phi/`: Contains Phi model checkpoints (e.g. Phi-3.5-mini-instruct).

### 2. ORT Graph Optimization Options (FlatBuffers)
Files ending in `.ort` represent serialized model graphs in ONNX Runtime's native **FlatBuffers** format.
*   **Fast Loading**: .ort models bypass WebGPU/WASM graph optimization step, accelerating session initialization times in web browsers by 3x to 5x.

---

## Asal Usul & Kredit / Origins & Credits

### Bahasa Indonesia
Aset-aset model ini di-host secara mandiri oleh **CraftThingy Digital Innovation (Alif Nurhidayat)**. Proyek ini dibangun di atas lisensi open-source hulu berikut:
1.  **Meta Llama**: Penyedia model Llama 3.2.
2.  **Alibaba Qwen**: Penyedia model Qwen 2.5.
3.  **Hugging Face**: Penyedia model SmolLM2.
4.  **OpenBMB**: Penyedia model MiniCPM5.

### English
These model assets are self-hosted by **CraftThingy Digital Innovation (Alif Nurhidayat)**. It is built upon the following open-source upstream works:
1.  **Meta Llama**: The developer of Llama 3.2 model family.
2.  **Alibaba Qwen**: The developer of Qwen 2.5 model family.
3.  **Hugging Face**: The developer of SmolLM2 model family.
4.  **OpenBMB**: The developer of MiniCPM5 model family.
