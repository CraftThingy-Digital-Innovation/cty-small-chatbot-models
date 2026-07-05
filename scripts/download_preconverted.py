import os
import argparse
import urllib.request

def download_file(url, dest_path):
    try:
        # Get expected content length
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            content_length = resp.info().get('Content-Length')
            expected_size = int(content_length) if content_length else None
            
        if expected_size and os.path.exists(dest_path):
            actual_size = os.path.getsize(dest_path)
            if actual_size == expected_size:
                print(f"[+] File already exists and matches expected size ({actual_size} bytes): {dest_path}")
                return
            else:
                print(f"[-] File size mismatch for {dest_path} (actual: {actual_size}, expected: {expected_size}). Redownloading...")

        print(f"[-] Downloading {url} -> {dest_path}")
        urllib.request.urlretrieve(url, dest_path)
        
        # Verify download size
        if expected_size:
            actual_size = os.path.getsize(dest_path)
            if actual_size != expected_size:
                raise ValueError(f"Download size mismatch. Expected {expected_size} bytes, got {actual_size} bytes.")
                
        print(f"[+] Successfully downloaded and verified {dest_path}")
    except Exception as e:
        print(f"[!] Failed to download: {e}")
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except:
                pass
        raise e

def main():
    parser = argparse.ArgumentParser(description="Download pre-converted ONNX models for cty-small-chatbot-models.")
    parser.add_argument("--model", type=str, choices=['smollm', 'llama', 'qwen', 'deepseek'], required=True,
                        help="The model to download: smollm, llama, qwen, or deepseek")
    args = parser.parse_args()

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    models_config = {
        "smollm": {
            "dir": "smollm",
            "repo": "onnx-community/SmolLM2-135M-Instruct-ONNX",
            "files": {
                "config.json": "resolve/main/config.json",
                "generation_config.json": "resolve/main/generation_config.json",
                "tokenizer.json": "resolve/main/tokenizer.json",
                "tokenizer_config.json": "resolve/main/tokenizer_config.json",
                "model_q4.onnx": "resolve/main/onnx/model_q4.onnx"
            }
        },
        "llama": {
            "dir": "llama",
            "repo": "onnx-community/Llama-3.2-1B-Instruct-ONNX",
            "files": {
                "config.json": "resolve/main/config.json",
                "generation_config.json": "resolve/main/generation_config.json",
                "tokenizer.json": "resolve/main/tokenizer.json",
                "tokenizer_config.json": "resolve/main/tokenizer_config.json",
                "model_q4.onnx": "resolve/main/onnx/model_q4.onnx",
                "model_q4.onnx_data": "resolve/main/onnx/model_q4.onnx_data"
            }
        },
        "qwen": {
            "dir": "qwen",
            "repo": "onnx-community/Qwen2.5-1.5B-Instruct",
            "files": {
                "config.json": "resolve/main/config.json",
                "generation_config.json": "resolve/main/generation_config.json",
                "tokenizer.json": "resolve/main/tokenizer.json",
                "tokenizer_config.json": "resolve/main/tokenizer_config.json",
                "model_q4.onnx": "resolve/main/onnx/model_q4.onnx"
            }
        },
        "deepseek": {
            "dir": "deepseek",
            "repo": "onnx-community/DeepSeek-R1-Distill-Qwen-1.5B-ONNX",
            "files": {
                "config.json": "resolve/main/config.json",
                "generation_config.json": "resolve/main/generation_config.json",
                "tokenizer.json": "resolve/main/tokenizer.json",
                "tokenizer_config.json": "resolve/main/tokenizer_config.json",
                "model_q4.onnx": "resolve/main/onnx/model_q4.onnx"
            }
        }
    }
    
    cfg = models_config[args.model]
    target_dir = os.path.join(repo_dir, cfg["dir"])
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"[-] Downloading pre-converted weights for '{args.model}' from HF repository '{cfg['repo']}'...")
    for filename, subpath in cfg["files"].items():
        url = f"https://huggingface.co/{cfg['repo']}/{subpath}"
        dest = os.path.join(target_dir, filename)
        download_file(url, dest)
        
    print(f"[+] Download of '{args.model}' completed successfully!")

if __name__ == "__main__":
    main()
