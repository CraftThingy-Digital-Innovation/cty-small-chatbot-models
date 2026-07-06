import os
import shutil
import urllib.request

# Dynamic chunked download function that supports authorization headers (for gated models like Gemma)
def download_file(url, dest_path):
    try:
        req = urllib.request.Request(url)
        # Retrieve HF token from environment if available
        token = os.environ.get('HF_TOKEN') or os.environ.get('HF_API_KEY')
        if token:
            req.add_header('Authorization', f'Bearer {token}')

        # Get expected content length
        try:
            with urllib.request.urlopen(req) as resp:
                content_length = resp.info().get('Content-Length')
                expected_size = int(content_length) if content_length else None
        except Exception as head_err:
            # If HEAD/initial GET fails, propagate error (e.g. 401 for gated models without token)
            raise head_err

        if expected_size and os.path.exists(dest_path):
            actual_size = os.path.getsize(dest_path)
            if actual_size == expected_size:
                print(f"[+] File already exists and matches expected size ({actual_size} bytes): {dest_path}")
                return
            else:
                print(f"[-] File size mismatch for {dest_path} (actual: {actual_size}, expected: {expected_size}). Redownloading...")

        print(f"[-] Downloading {url} -> {dest_path}")
        with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        # Verify download size
        if expected_size:
            actual_size = os.path.getsize(dest_path)
            if actual_size != expected_size:
                raise ValueError(f"Download size mismatch. Expected {expected_size} bytes, got {actual_size} bytes.")

        print(f"[+] Successfully downloaded and verified {dest_path}")
    except Exception as e:
        print(f"[!] Failed to download {url}: {e}")
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except:
                pass
        raise e

def reorganize_existing_model(repo_dir, category, model_name, files_to_move, split_data_file=None):
    category_dir = os.path.join(repo_dir, category)
    model_dir = os.path.join(category_dir, model_name)
    converted_dir = os.path.join(model_dir, "converted")
    original_dir = os.path.join(model_dir, "original")

    os.makedirs(converted_dir, exist_ok=True)
    os.makedirs(original_dir, exist_ok=True)

    print(f"\n[-] Reorganizing '{category}' -> '{model_name}'...")

    # Move files from root category directory to new paths
    for f in files_to_move:
        src = os.path.join(category_dir, f)
        if os.path.exists(src):
            # Copy configuration/tokenizer metadata to original/
            if f.endswith('.json') or f.endswith('.txt'):
                shutil.copy2(src, os.path.join(original_dir, f))
                print(f"  [+] Copied configuration metadata to original: {f}")
            
            # Move the file to converted/
            dest = os.path.join(converted_dir, f)
            shutil.move(src, dest)
            print(f"  [+] Moved file to converted: {f}")

    if split_data_file:
        src = os.path.join(category_dir, split_data_file)
        if os.path.exists(src):
            dest = os.path.join(converted_dir, split_data_file)
            shutil.move(src, dest)
            print(f"  [+] Moved split data file to converted: {split_data_file}")

    print(f"[+] Reorganization of '{model_name}' completed.")

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Reorganize existing models that were already downloaded in the category root directory
    common_files = ["config.json", "generation_config.json", "tokenizer.json", "tokenizer_config.json", "model_q4.onnx"]
    
    reorganize_existing_model(repo_dir, "smollm", "SmolLM2-135M-Instruct", common_files)
    reorganize_existing_model(repo_dir, "llama", "Llama-3.2-1B-Instruct", common_files, "model_q4.onnx_data")
    reorganize_existing_model(repo_dir, "qwen", "Qwen2.5-1.5B-Instruct", common_files)
    reorganize_existing_model(repo_dir, "deepseek", "DeepSeek-R1-Distill-Qwen-1.5B", common_files)

    # 2. Download missing models directly into the new folder structure
    print("\n[-] Starting downloads for new models...")

    # A. MiniCPM5-1B GGUF Model (Ollama/llama.cpp compatible)
    minicpm_dir = os.path.join(repo_dir, "minicpm", "MiniCPM5-1B")
    minicpm_conv = os.path.join(minicpm_dir, "converted")
    minicpm_orig = os.path.join(minicpm_dir, "original")
    os.makedirs(minicpm_conv, exist_ok=True)
    os.makedirs(minicpm_orig, exist_ok=True)

    print("\n[-] Processing MiniCPM5-1B...")
    try:
        gguf_url = "https://huggingface.co/openbmb/MiniCPM5-1B-GGUF/resolve/main/MiniCPM5-1B-Q4_K_M.gguf"
        download_file(gguf_url, os.path.join(minicpm_conv, "MiniCPM5-1B-Q4_K_M.gguf"))
        
        # Download original configs as reference
        orig_config_url = "https://huggingface.co/openbmb/MiniCPM5-1B/resolve/main/config.json"
        download_file(orig_config_url, os.path.join(minicpm_orig, "config.json"))
        print("[+] MiniCPM5-1B completed.")
    except Exception as e:
        print(f"[!] MiniCPM5-1B processing failed: {e}")

    # B. Phi-3.5-mini-instruct (ONNX format)
    phi_dir = os.path.join(repo_dir, "phi", "Phi-3.5-mini-instruct")
    phi_conv = os.path.join(phi_dir, "converted")
    phi_orig = os.path.join(phi_dir, "original")
    os.makedirs(phi_conv, exist_ok=True)
    os.makedirs(phi_orig, exist_ok=True)

    print("\n[-] Processing Phi-3.5-mini-instruct...")
    try:
        phi_repo = "onnx-community/Phi-3.5-mini-instruct-onnx-web"
        phi_files = ["config.json", "generation_config.json", "tokenizer.json", "tokenizer_config.json"]
        
        for f in phi_files:
            url = f"https://huggingface.co/{phi_repo}/resolve/main/{f}"
            download_file(url, os.path.join(phi_conv, f))
            # Save a copy in original
            shutil.copy2(os.path.join(phi_conv, f), os.path.join(phi_orig, f))
            
        # Download model weights (with renaming to model_q4.onnx)
        download_file(f"https://huggingface.co/{phi_repo}/resolve/main/onnx/model_q4f16.onnx", os.path.join(phi_conv, "model_q4.onnx"))
        download_file(f"https://huggingface.co/{phi_repo}/resolve/main/onnx/model_q4f16.onnx_data", os.path.join(phi_conv, "model_q4.onnx_data"))
        print("[+] Phi-3.5-mini-instruct completed.")
    except Exception as e:
        print(f"[!] Phi-3.5-mini-instruct processing failed: {e}")

    # C. Gemma-2-2b-it (ONNX format - gated)
    gemma_dir = os.path.join(repo_dir, "gemma", "gemma-2-2b-it")
    gemma_conv = os.path.join(gemma_dir, "converted")
    gemma_orig = os.path.join(gemma_dir, "original")
    os.makedirs(gemma_conv, exist_ok=True)
    os.makedirs(gemma_orig, exist_ok=True)

    print("\n[-] Processing Gemma-2-2b-it...")
    gemma_token = os.environ.get('HF_TOKEN') or os.environ.get('HF_API_KEY')
    if not gemma_token:
        print("[WARNING] No HF_TOKEN found in environment. Downloading Gemma-2-2b-it may fail because it is a gated model.")

    try:
        gemma_repo = "onnx-community/gemma-2-2b-it-ONNX"
        gemma_files = ["config.json", "generation_config.json", "tokenizer.json", "tokenizer_config.json"]
        
        for f in gemma_files:
            url = f"https://huggingface.co/{gemma_repo}/resolve/main/{f}"
            download_file(url, os.path.join(gemma_conv, f))
            shutil.copy2(os.path.join(gemma_conv, f), os.path.join(gemma_orig, f))
            
        # Download model weights
        download_file(f"https://huggingface.co/{gemma_repo}/resolve/main/onnx/model_q4.onnx", os.path.join(gemma_conv, "model_q4.onnx"))
        print("[+] Gemma-2-2b-it completed.")
    except Exception as e:
        print(f"[!] Gemma-2-2b-it processing failed: {e}")
        print("[!] Note: Gemma-2-2b-it requires a valid Hugging Face API token in your HF_TOKEN environment variable.")

    print("\n[+] Reorganization and downloads complete!")

if __name__ == "__main__":
    main()
