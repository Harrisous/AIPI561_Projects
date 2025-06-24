from llama_cpp import Llama

llm = Llama(
    model_path="models\\mixtral-8x7b-instruct-v0.1.Q3_K_M.gguf",
    n_ctx=512,
    n_threads=4,
    n_gpu_layers=-1  # Use -1 to load all layers to GPU (if supported)
)

output = llm("[INST] Hello, who are you? [/INST]", max_tokens=32)
print(output['choices'][0]['text'])