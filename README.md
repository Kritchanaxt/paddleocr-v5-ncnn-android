# paddleocr-v5-ncnn-android
How to convert PaddleOCR v5 to NCNN for Android

## 🚀 How to Reproduce / Continue Developing

If you want to modify the pipeline (e.g., convert new models or use different shape constraints), you can easily re-run the conversions.

### Setup Environment
1. Clone this repository.
2. Ensure you have CMake, Protobuf, and Git installed.
```bash
brew install cmake protobuf git
```
3. Setup Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install paddlepaddle paddle2onnx onnx onnxsim
```
4. Build NCNN Conversion Tools:
```bash
git clone https://github.com/Tencent/ncnn.git
cd ncnn/build
cmake -DCMAKE_BUILD_TYPE=Release -DNCNN_BUILD_TOOLS=ON -DNCNN_VULKAN=OFF ..
make -j8
cd ../..
```

### Running the Conversion Script
We provide a handy python script: `convert_pipeline.py`. Once the models and NCNN tools are in place, simply run:
```bash
source venv/bin/activate
python convert_pipeline.py
```
This script will automatically execute:
1. `paddle2onnx` (Raw to ONNX)
2. `onnxsim` (Simplification & Static Shape Enforcement)
3. `onnx2ncnn` (ONNX to NCNN framework)
4. `ncnnoptimize` (Reduce inference size with FP16)
