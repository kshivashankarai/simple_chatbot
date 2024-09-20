from huggingface_hub import hf_hub_download

model_name = 'TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF'

model_file = 'tinyllama-1.1b-chat-v1.0.Q8_0.gguf'

model_path = hf_hub_download(model_name, filename=model_file, local_dir='/home/shiva/DeveloperDen/Python/chat_with_postgres/model')