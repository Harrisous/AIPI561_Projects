from llama_cpp import Llama

llm = Llama(
    model_path="models/mixtral-8x7b-instruct-v0.1.Q3_K_M.gguf",
    n_ctx=512,
    n_threads=1,
    n_gpu_layers=0
)

output = llm("Hello", max_tokens=10)
print(output['choices'][0]['text'])