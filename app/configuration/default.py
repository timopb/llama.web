MODEL = "(put your model name here)"

# Stopwords for instruct and vicuna style prompts
STOP_WORDS = ["### response:", "assistant:"]

# Format: ["(promt template)", (cursor position inside prompt for user input)]
VICUNA_PROMPT_TEMPLATE = ["You are a helpful AI assistant.\\n\\nUSER: \\n\\nASSISTANT:", 39]
INSTRUCT_PROMPT_TEMPLATE = ["\\n\\n### RESPONSE:", 0]
STORY_PROMPT_TEMPLATE = ["You are a storyteller. Your writing is vivid, exentive and very detailed. Extract the character traits from the user's input but don't name them in your story directly. Instead weave them into the story.\\n\\nUSER: Write a story about \\n\\nASSISTANT:",  231]

TEMPERATURE = 0.3
TOP_P=0.6
TOP_K=40
REPETATION_PENALTY=1.176

CONTEXT_TOKENS = 2048
MAX_RESPONSE_TOKENS = 8192
