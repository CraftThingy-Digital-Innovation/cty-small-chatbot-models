import os
import urllib.request

def download_file(url, dest_path):
    print(f"[-] Downloading {url} -> {dest_path}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"[+] Successfully downloaded to {dest_path}")
    except Exception as e:
        print(f"[!] Failed to download: {e}")
        raise e

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(repo_dir, "smollm")
    os.makedirs(target_dir, exist_ok=True)
    
    files = {
        "config.json": "https://huggingface.co/onnx-community/SmolLM2-135M-Instruct-ONNX/raw/main/config.json",
        "generation_config.json": "https://huggingface.co/onnx-community/SmolLM2-135M-Instruct-ONNX/raw/main/generation_config.json",
        "tokenizer.json": "https://huggingface.co/onnx-community/SmolLM2-135M-Instruct-ONNX/raw/main/tokenizer.json",
        "tokenizer_config.json": "https://huggingface.co/onnx-community/SmolLM2-135M-Instruct-ONNX/raw/main/tokenizer_config.json",
        "model_q4.onnx": "https://huggingface.co/onnx-community/SmolLM2-135M-Instruct-ONNX/resolve/main/onnx/model_q4.onnx"
    }
    
    for name, url in files.items():
        dest = os.path.join(target_dir, name)
        download_file(url, dest)
        
    print("[+] SmolLM2-135M-Instruct ONNX download completed successfully!")

if __name__ == "__main__":
    main()
