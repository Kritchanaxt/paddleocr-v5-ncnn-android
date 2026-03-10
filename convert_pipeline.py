import os
import sys

def run_cmd(cmd):
    print(f"Running: {cmd}\n")
    ret = os.system(cmd)
    if ret != 0:
        print(f"Error executing: {cmd}")
        sys.exit(1)

print("=== 1. Convert PaddleOCR Models to ONNX ===")
run_cmd('paddle2onnx --model_dir models/paddle/en --model_filename inference.json --params_filename inference.pdiparams --save_file models/onnx/rec_en.onnx --opset_version 11')
run_cmd('paddle2onnx --model_dir models/paddle/th --model_filename inference.json --params_filename inference.pdiparams --save_file models/onnx/rec_th.onnx --opset_version 11')

print("\n=== 2. Simplify ONNX and Fix Dynamic Shape ===")
run_cmd('onnxsim models/onnx/rec_en.onnx models/onnx/rec_en_sim_fixed.onnx --overwrite-input-shape x:1,3,48,320')
run_cmd('onnxsim models/onnx/rec_th.onnx models/onnx/rec_th_sim_fixed.onnx --overwrite-input-shape x:1,3,48,320')

print("\n=== 3. Convert ONNX to NCNN ===")
run_cmd('./ncnn/build/tools/onnx/onnx2ncnn models/onnx/rec_en_sim_fixed.onnx models/ncnn/en/rec_en.param models/ncnn/en/rec_en.bin')
run_cmd('./ncnn/build/tools/onnx/onnx2ncnn models/onnx/rec_th_sim_fixed.onnx models/ncnn/th/rec_th.param models/ncnn/th/rec_th.bin')

print("\n=== 4. Optimize NCNN Models ===")
run_cmd('./ncnn/build/tools/ncnnoptimize models/ncnn/en/rec_en.param models/ncnn/en/rec_en.bin models/ncnn/en/rec_en_opt.param models/ncnn/en/rec_en_opt.bin 65536')
run_cmd('./ncnn/build/tools/ncnnoptimize models/ncnn/th/rec_th.param models/ncnn/th/rec_th.bin models/ncnn/th/rec_th_opt.param models/ncnn/th/rec_th_opt.bin 65536')

print("Pipeline completed successfully!")