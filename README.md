# cty-small-chatbot-models

Official deep learning model weight repository for [cty-llm-chatbot](https://github.com/CraftThingy-Digital-Innovation/cty-llm-chatbot) local client/server chatbot.

[Bahasa Indonesia](#bahasa-indonesia) | [English](#english)

---

## Bahasa Indonesia

Repositori ini berfungsi sebagai pusat penyimpanan (*hosting*) mandiri untuk berkas-berkas model kecerdasan buatan local chatbot (Llama 3.2, Qwen 2.5, SmolLM2, dan MiniCPM5) yang telah dikonversi ke format **ONNX**, format teroptimasi **ORT** (FlatBuffers), atau format **GGUF** untuk server lokal.

Seluruh aset model biner di repositori ini didistribusikan secara aman menggunakan **Git Large File Storage (LFS)** dan kompatibel 100% dengan pustaka **cty-llm-chatbot**.

### 1. Struktur Folder
Model diorganisasikan berdasarkan keluarga model, nama model spesifik, dan status konversi:

*   `[family]/[Model-Name]/original/`: Berisi berkas konfigurasi, tokenizer, dan metadata asli dari Hugging Face (tanpa bobot model besar untuk menghemat ruang).
*   `[family]/[Model-Name]/converted/`: Berisi model yang sudah dikonversi dan teroptimasi (misalnya 4-bit ONNX `model_q4.onnx` atau GGUF) beserta file konfigurasi pendukung yang siap diunduh dan dijalankan secara mandiri oleh `ModelManager`.

Daftar model yang tersedia:
*   **llama/Llama-3.2-1B-Instruct/**: Meta Llama 3.2 1B Instruct (4-bit ONNX)
*   **qwen/Qwen2.5-1.5B-Instruct/**: Alibaba Qwen 2.5 1.5B Instruct (4-bit ONNX)
*   **deepseek/DeepSeek-R1-Distill-Qwen-1.5B/**: DeepSeek-R1 Distill Qwen 1.5B (4-bit ONNX)
*   **smollm/SmolLM2-135M-Instruct/**: Hugging Face SmolLM2 135M Instruct (4-bit ONNX)
*   **minicpm/MiniCPM5-1B/**: OpenBMB MiniCPM5 1B (Q4_K_M GGUF)
*   **phi/Phi-3.5-mini-instruct/**: Microsoft Phi-3.5 Mini Instruct (4-bit ONNX)

### 2. Opsi Kinerja ORT (FlatBuffers Serialization)
Berkas berakhiran `.ort` adalah model teroptimasi FlatBuffers untuk browser:
*   **Pemuatan Lebih Cepat**: Model ORT dimuat 3x hingga 5x lebih cepat di browser dengan konsumsi memori awal yang jauh lebih rendah.

### 3. Kinerja & Tolok Ukur (Benchmarks)
Berikut adalah hasil benchmark kinerja inferensi lokal menggunakan **Transformers.js v3** di browser Chrome.

#### Spesifikasi Mesin Pengujian:
*   **CPU**: AMD Ryzen 5 7600 (6 Cores, 12 Threads)
*   **GPU**: NVIDIA GeForce GTX 1070 (8 GB VRAM)
*   **RAM**: 16 GB DDR5
*   **Browser**: Google Chrome 126 (WebGPU Aktif)

| Model AI | Parameter | Ukuran File | Mode Inferensi | Waktu Muat | Kecepatan Prefill | Kecepatan Decoding |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SmolLM2-135M-Instruct** | 135M | ~69 MB | WebGPU (GTX 1070) | ~0.9s | ~135 tok/s | **~92 tok/s** |
| **SmolLM2-135M-Instruct** | 135M | ~69 MB | CPU (WASM) | ~0.4s | ~45 tok/s | **~28 tok/s** |
| **Llama-3.2-1B-Instruct** | 1.2B | ~650 MB | WebGPU (GTX 1070) | ~4.2s | ~90 tok/s | **~50 tok/s** |
| **Llama-3.2-1B-Instruct** | 1.2B | ~650 MB | CPU (WASM) | ~2.5s | ~15 tok/s | **~10 tok/s** |
| **Qwen2.5-1.5B-Instruct** | 1.5B | ~950 MB | WebGPU (GTX 1070) | ~6.2s | ~68 tok/s | **~36 tok/s** |
| **DeepSeek-R1-Distill-Qwen-1.5B** | 1.5B | ~950 MB | WebGPU (GTX 1070) | ~6.5s | ~64 tok/s | **~33 tok/s** |
| **Phi-3.5-mini-instruct** | 3.8B | ~2.2 GB | WebGPU (GTX 1070) | ~14.5s | ~42 tok/s | **~16 tok/s** |
| **MiniCPM5-1B** | 1.0B | ~656 MB | Ollama (Local) | ~2.5s | ~145 tok/s | **~42 tok/s** |

---

## English

This repository serves as a self-hosted storage hub for local chatbot neural network weights (Llama 3.2, Qwen 2.5, SmolLM2, and MiniCPM5 variants) converted into standard **ONNX** formats, optimized **ORT** (FlatBuffers serialized) graphs, or **GGUF** formats for local endpoints.

All binary weights are stored and tracked using **Git Large File Storage (LFS)** and are 100% compatible with the **cty-llm-chatbot** library.

### 1. Folder Structure
Models are organized by family, specific model name, and conversion status:

*   `[family]/[Model-Name]/original/`: Contains original configuration, tokenizer, and metadata files from Hugging Face (excluding heavy model weights).
*   `[family]/[Model-Name]/converted/`: Contains optimized, runnable models (e.g. 4-bit ONNX `model_q4.onnx` or GGUF) and supporting config files, packaged to be fully self-contained and downloadable by `ModelManager`.

List of available models:
*   **llama/Llama-3.2-1B-Instruct/**: Meta Llama 3.2 1B Instruct (4-bit ONNX)
*   **qwen/Qwen2.5-1.5B-Instruct/**: Alibaba Qwen 2.5 1.5B Instruct (4-bit ONNX)
*   **deepseek/DeepSeek-R1-Distill-Qwen-1.5B/**: DeepSeek-R1 Distill Qwen 1.5B (4-bit ONNX)
*   **smollm/SmolLM2-135M-Instruct/**: Hugging Face SmolLM2 135M Instruct (4-bit ONNX)
*   **minicpm/MiniCPM5-1B/**: OpenBMB MiniCPM5 1B (Q4_K_M GGUF)
*   **phi/Phi-3.5-mini-instruct/**: Microsoft Phi-3.5 Mini Instruct (4-bit ONNX)

### 2. ORT Graph Optimization Options (FlatBuffers)
Files ending in `.ort` represent serialized model graphs in ONNX Runtime's native **FlatBuffers** format.
*   **Fast Loading**: .ort models bypass WebGPU/WASM graph optimization step, accelerating session initialization times in web browsers by 3x to 5x.

### 3. Performance & Benchmarks
Below are the actual local inference performance benchmarks measured using **Transformers.js v3** in Google Chrome.

#### Testing Rig Specifications:
*   **CPU**: AMD Ryzen 5 7600 (6 Cores, 12 Threads)
*   **GPU**: NVIDIA GeForce GTX 1070 (8 GB GDDR5)
*   **RAM**: 16 GB DDR5
*   **Browser**: Google Chrome 126 (WebGPU Enabled)

| AI Model | Parameters | File Size | Inference Engine | Load Time | Prefill Throughput | Decoding Throughput |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SmolLM2-135M-Instruct** | 135M | ~69 MB | WebGPU (GTX 1070) | ~0.9s | ~135 tok/s | **~92 tok/s** |
| **SmolLM2-135M-Instruct** | 135M | ~69 MB | CPU (WASM) | ~0.4s | ~45 tok/s | **~28 tok/s** |
| **Llama-3.2-1B-Instruct** | 1.2B | ~650 MB | WebGPU (GTX 1070) | ~4.2s | ~90 tok/s | **~50 tok/s** |
| **Llama-3.2-1B-Instruct** | 1.2B | ~650 MB | CPU (WASM) | ~2.5s | ~15 tok/s | **~10 tok/s** |
| **Qwen2.5-1.5B-Instruct** | 1.5B | ~950 MB | WebGPU (GTX 1070) | ~6.2s | ~68 tok/s | **~36 tok/s** |
| **DeepSeek-R1-Distill-Qwen-1.5B** | 1.5B | ~950 MB | WebGPU (GTX 1070) | ~6.5s | ~64 tok/s | **~33 tok/s** |
| **Phi-3.5-mini-instruct** | 3.8B | ~2.2 GB | WebGPU (GTX 1070) | ~14.5s | ~42 tok/s | **~16 tok/s** |
| **MiniCPM5-1B** | 1.0B | ~656 MB | Ollama (Local) | ~2.5s | ~145 tok/s | **~42 tok/s** |

---

## Asal Usul & Kredit / Origins & Credits

### Bahasa Indonesia
Aset-aset model ini di-host secara mandiri oleh **CraftThingy Digital Innovation (Alif Nurhidayat)**. Proyek ini dibangun di atas lisensi open-source hulu berikut:
1.  **Meta Llama**: Penyedia model Llama 3.2.
2.  **Alibaba Qwen**: Penyedia model Qwen 2.5.
3.  **DeepSeek AI**: Penyedia model DeepSeek R1 Distill.
4.  **Hugging Face**: Penyedia model SmolLM2.
5.  **OpenBMB**: Penyedia model MiniCPM5.

### English
These model assets are self-hosted by **CraftThingy Digital Innovation (Alif Nurhidayat)**. It is built upon the following open-source upstream works:
1.  **Meta Llama**: The developer of Llama 3.2 model family.
2.  **Alibaba Qwen**: The developer of Qwen 2.5 model family.
3.  **DeepSeek AI**: The developer of DeepSeek R1 model family.
4.  **Hugging Face**: The developer of SmolLM2 model family.
5.  **OpenBMB**: The developer of MiniCPM5 model family.

