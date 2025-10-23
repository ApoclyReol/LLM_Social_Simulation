# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
# (保持不变)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY_HERE")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY_HERE")
ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY", "YOUR_ZHIPUAI_API_KEY_HERE") # 新增
BAIDU_API_KEY = os.getenv("BAIDU_API_KEY", "YOUR_BAIDU_API_KEY_HERE")       # 新增
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY", "YOUR_BAIDU_SECRET_KEY_HERE") # 新增

# --- API Base URLs ---
# 添加Base URL配置，同样建议用环境变量设置
# 在 .env 文件中添加类似:
# OPENAI_BASE_URL="https://api.your-proxy.com/v1"
# ZHIPUAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4/" # 智谱官方地址示例
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", None) # 默认None表示使用官方地址
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", None)
GOOGLE_BASE_URL = os.getenv("GOOGLE_BASE_URL", None) # Google Gemini可能不需要设置base_url，取决于库
ZHIPUAI_BASE_URL = os.getenv("ZHIPUAI_BASE_URL", None) # 新增
BAIDU_BASE_URL = os.getenv("BAIDU_BASE_URL", None)     # 新增

# --- Model Names ---
# (可以添加更多国内模型)
MODELS_TO_RUN = {
    "openai": ["gpt-4o", "gpt-3.5-turbo"],
    # "anthropic": ["claude-3-opus-20240229"],
    # "google": ["gemini-1.5-pro-latest"],
    # "zhipuai": ["glm-4"], # 新增智谱模型
    # "baidu": ["ernie-bot-4.0"] # 新增文心模型 (模型名称可能需要确认)
}

# --- File Paths ---
# (保持不变)
PROMPT_DIR = "prompts"
DATA_DIR = "data"
OUTPUT_DIR = "outputs"

PROMPT_FILES = {
    "general": os.path.join(PROMPT_DIR, "general_persona_prompt.txt"),
    "silicon": os.path.join(PROMPT_DIR, "silicon_persona_prompt.txt"),
    "cognitive": os.path.join(PROMPT_DIR, "cognitive_persona_prompt.txt"),
}

DATA_FILES = {
    "survey": os.path.join(DATA_DIR, "survey.json"),
    "personachat": os.path.join(DATA_DIR, "personachat_snippets.json"),
    "cgss": os.path.join(DATA_DIR, "cgss_demographics.csv"),
    "cognitive": os.path.join(DATA_DIR, "cognitive_profiles.json"),
}

# --- Simulation Parameters ---
# (保持不变)
TEMPERATURE = 0.8
MAX_TOKENS_PER_RESPONSE = 500
REQUEST_DELAY = 1

# --- Persona Generation Parameters ---
# (保持不变)
NUM_PERSONACHAT_SENTENCES = 5

# --- Output Files ---
# (保持不变)
OUTPUT_FILES = {
    "general": os.path.join(OUTPUT_DIR, "results_general_persona.csv"),
    "silicon": os.path.join(OUTPUT_DIR, "results_silicon_persona.csv"),
    "cognitive": os.path.join(OUTPUT_DIR, "results_cognitive_persona.csv"),
}

# --- Ensure output directory exists ---
# (保持不变)
os.makedirs(OUTPUT_DIR, exist_ok=True)