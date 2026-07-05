import os
import sys
import subprocess
import argparse
import shutil

def check_dependencies():
    """Checks and prompts to install required Python packages for ONNX model export."""
    requirements = ['optimum', 'onnxruntime', 'onnx', 'huggingface_hub']
    missing = []
    for req in requirements:
        try:
            __import__(req)
        except ImportError:
            missing.append(req)
            
    if missing:
        print(f"[!] Missing required packages: {', '.join(missing)}")
        install = input("[-] Would you like to install them now? (y/n): ").strip().lower()
        if install == 'y':
            print("[-] Installing packages via pip...")
            # Install optimum with exponents
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'optimum[exporters]', 'onnxruntime', 'onnx', 'huggingface_hub'], check=True)
            print("[+] Installation completed successfully!")
        else:
            print("[!] Please install the packages manually using:")
            print("    pip install optimum[exporters] onnxruntime onnx huggingface_hub")
            sys.exit(1)

def quantize_onnx_model(model_path, quantized_path):
    """Applies dynamic 8-bit quantization to the exported ONNX model."""
    print(f"[-] Quantizing model: {model_path} -> {quantized_path}")
    try:
        from onnxruntime.quantization import quantize_dynamic, QuantType
        quantize_dynamic(
            model_input=model_path,
            model_output=quantized_path,
            weight_type=QuantType.QUInt8
        )
        print("[+] Quantization finished successfully!")
        return True
    except Exception as e:
        print(f"[!] Quantization failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Download and convert LLM models to ONNX format for cty-small-chatbot-models.")
    parser.add_argument("--model", type=str, required=True, 
                        help="Hugging Face model ID (e.g. 'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', 'meta-llama/Llama-3.2-1B-Instruct')")
    parser.add_argument("--category", type=str, choices=['llama', 'qwen', 'smollm', 'minicpm', 'gemma', 'phi'], required=True,
                        help="Model family directory category")
    parser.add_argument("--quantize", action="store_true", help="Apply 8-bit dynamic quantization to the output model")
    
    args = parser.parse_args()
    
    check_dependencies()
    
    # Target directory setup
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    target_dir = os.path.join(repo_dir, args.category)
    
    print(f"[-] Target Directory: {target_dir}")
    os.makedirs(target_dir, exist_ok=True)
    
    # Temp export directory
    temp_dir = os.path.join(repo_dir, "temp_export")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"[-] Exporting model '{args.model}' via Optimum CLI...")
    try:
        # Run optimum-cli export command
        cmd = [
            "optimum-cli", "export", "onnx",
            "--model", args.model,
            "--task", "text-generation-with-past",
            temp_dir
        ]
        print(f"[-] Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print("[+] Model exported to ONNX successfully.")
        
        # Check files in temp folder and move to target folder
        for file_name in os.listdir(temp_dir):
            src_file = os.path.join(temp_dir, file_name)
            
            # If quantization is checked and this is a main model file, quantize it
            if args.quantize and file_name.endswith("model.onnx"):
                dest_file = os.path.join(target_dir, file_name.replace(".onnx", "_quantized.onnx"))
                quantize_onnx_model(src_file, dest_file)
            else:
                dest_file = os.path.join(target_dir, file_name)
                print(f"[-] Copying: {file_name} -> {dest_file}")
                shutil.copy2(src_file, dest_file)
                
        print(f"[+] All files processed and saved into '{args.category}/' directory!")
        
    except subprocess.CalledProcessError as err:
        print(f"[!] Optimum export failed with exit code: {err.returncode}")
    except Exception as e:
        print(f"[!] Error during conversion workflow: {e}")
    finally:
        # Cleanup temp files
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
