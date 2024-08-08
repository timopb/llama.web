# MODEL = "nous-hermes/nous-hermes-llama2-13b.gguf.q4_k_m.bin"
# MODEL = "nous-hermes/nous-hermes-llama2-7b.gguf.q4_k_m.bin"
# MODEL = "WizardLM/WizardLM-13B-V1.0-Uncensored.gguf.q4_k_m.bin"
# MODEL = "WizardLM/WizardLM-7B-V1.0-Uncensored.gguf.q4_k_m.bin"
MODEL = "microsoft/Phi-3-mini-4k-instruct.q4_k_m.gguf"

# Stopwords for instruct and vicuna style prompts
STOP_WORDS = ["User:", "Assistant:", "user:", "assistant:", "USER:", "ASSISTANT:", "<|system|>", "<|user|>", "<|assistant|>"]

# Format: ["(autcomplete prefix)","(promt template)", (cursor position inside prompt for user input)]
PROMPT_TEMPLATES = [
    ["vic",   "You are a helpful AI assistant.\\n\\nUSER: \\n\\nASSISTANT:", 39],
    ["##",    "\\n\\n### RESPONSE:", 0],
    ["story", "You are a storyteller. Your writing is vivid, exentive and very detailed. Extract the character traits from the user's input but don't name them in your story directly. Instead weave them into the story.\\n\\nUSER: Write a story about \\n\\nASSISTANT:",  231],
    ["inst", "[INST]\\n<<SYS>>You are a helpfull, respectful and honest assistant<</SYS>>\\n\\n[/INST]\\n", 74],
    ["phi", "<|system|>\\nYou are a helpful assistant.<|end|>\\n<|user|>\\n<|end|>\\n<|assistant|>", 56]
]

TEMPERATURE = 0.5
TOP_P=0.6
TOP_K=40
REPETATION_PENALTY=1.176

CONTEXT_TOKENS = 2048
MAX_RESPONSE_TOKENS = 8192

# For a GTX 1660TI with 6GB RAM use 32 for 7B, or 16 for 13B Models
GPU_LAYERS=33
