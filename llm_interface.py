# llm_interface.py
import time
import config
from openai import OpenAI, RateLimitError, APIError
# from anthropic import Anthropic, APIError as AnthropicAPIError
# import google.generativeai as genai
# import zhipuai # 示例：需要 pip install zhipuai
# import qianfan # 示例：需要 pip install qianfan

# --- OpenAI API Call ---
def call_openai_api(prompt, model_name, api_key, base_url, temperature, max_tokens):
    """调用OpenAI API (支持自定义 base_url)"""
    client_args = {"api_key": api_key}
    if base_url:
        client_args["base_url"] = base_url
        print(f"  使用自定义OpenAI Base URL: {base_url}")
    else:
         print(f"  使用官方OpenAI API地址。")


    client = OpenAI(**client_args)
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "你是一个正在参与社会调查的受访者。"},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except RateLimitError:
        print(f"速率限制错误，等待{config.REQUEST_DELAY * 5}秒后重试...")
        time.sleep(config.REQUEST_DELAY * 5)
        return call_openai_api(prompt, model_name, api_key, base_url, temperature, max_tokens) # 重试
    except APIError as e:
        print(f"OpenAI API 错误 ({model_name} @ {base_url or 'official'}): {e}")
        return None
    except Exception as e:
        print(f"调用OpenAI ({model_name}) 时发生未知错误: {e}")
        return None

# --- Anthropic API Call (示例，需根据实际库调整base_url用法) ---
def call_anthropic_api(prompt, model_name, api_key, base_url, temperature, max_tokens):
    """(示例) 调用Anthropic API (需确认如何设置 base_url)"""
    # client_args = {"api_key": api_key}
    # if base_url:
    #     client_args["base_url"] = base_url # 确认Anthropic库是否支持这样设置
    # client = Anthropic(**client_args)
    # try:
    #     response = client.messages.create(...)
    #     return response.content[0].text.strip()
    # except AnthropicAPIError as e:
    #      print(f"Anthropic API 错误 ({model_name} @ {base_url or 'official'}): {e}")
    #      return None
    # except Exception as e:
    #     print(f"调用Anthropic ({model_name}) 时发生未知错误: {e}")
    #     return None
    print(f"Anthropic API ({model_name}) 调用未实现或未更新Base URL支持。")
    return None

# --- Google Gemini API Call (通常不需要base_url) ---
def call_google_api(prompt, model_name, api_key, base_url, temperature, max_tokens):
    """(示例) 调用Google Gemini API"""
    # Google的库通常通过 configure 直接设置api_key，base_url不是标准参数
    # if base_url:
    #    print(f"警告：Google Gemini API 通常不直接支持 base_url 设置。将尝试使用默认地址。")
    # genai.configure(api_key=api_key)
    # model = genai.GenerativeModel(model_name)
    # try:
    #     response = model.generate_content(...)
    #     return response.text.strip()
    # except Exception as e:
    #     print(f"Google Gemini API 错误 ({model_name}): {e}")
    #     return None
    print(f"Google Gemini API ({model_name}) 调用未实现。")
    return None

# --- 智谱 API Call (示例) ---
def call_zhipuai_api(prompt, model_name, api_key, base_url, temperature, max_tokens):
    """(示例) 调用智谱AI API (支持自定义 base_url)"""
    # try:
    #     # 注意：智谱的库可能在初始化或调用时有不同的方式设置base_url
    #     zhipuai.api_key = api_key
    #     if base_url:
    #         zhipuai.api_base = base_url # 假设库是这样设置的，请查阅文档
    #         print(f"  使用自定义智谱 Base URL: {base_url}")
    #     else:
    #          print(f"  使用官方智谱 API地址。")

    #     response = zhipuai.model_api.invoke(
    #         model=model_name,
    #         prompt=[{"role": "user", "content": prompt}],
    #         temperature=temperature,
    #         # max_tokens 可能有不同参数名
    #     )
    #     if response and response['code'] == 200:
    #          # 解析 response['data']['choices'][0]['content'] 等，根据实际返回结构
    #          # return parsed_content
    #          pass
    #     else:
    #          print(f"智谱API返回错误: {response}")
    #          return None

    # except Exception as e:
    #     print(f"调用智谱AI ({model_name}) 时发生错误: {e}")
    #     return None
    print(f"智谱AI API ({model_name}) 调用未实现。")
    return None

# --- 百度文心 API Call (示例) ---
def call_baidu_api(prompt, model_name, api_key, secret_key, base_url, temperature, max_tokens):
     """(示例) 调用百度文心 API (可能支持自定义 endpoint)"""
     # try:
     #     # 百度文心通常需要 API Key 和 Secret Key
     #     # 它的库(qianfan)可能通过环境变量或配置对象设置认证和endpoint
     #     # os.environ["QIANFAN_AK"] = api_key
     #     # os.environ["QIANFAN_SK"] = secret_key
     #     # if base_url:
     #     #     os.environ["QIANFAN_BASE_URL"] = base_url # 假设环境变量可以设置
     #     #     print(f"  使用自定义文心 Base URL: {base_url}")
     #     # else:
     #     #     print(f"  使用官方文心 API地址。")

     #     chat_comp = qianfan.ChatCompletion()
     #     resp = chat_comp.do(
     #         model=model_name, # 可能需要映射为百度特定的模型标识符
     #         messages=[{"role": "user", "content": prompt}],
     #         temperature=temperature,
     #         # max_tokens 可能有不同参数名
     #     )
     #     # 解析 resp['result']
     #     # return parsed_content
     #     pass
     # except Exception as e:
     #      print(f"调用百度文心 ({model_name}) 时发生错误: {e}")
     #      return None
     print(f"百度文心 API ({model_name}) 调用未实现。")
     return None


# --- 主接口函数 ---
def get_llm_response(prompt, model_name, temperature=config.TEMPERATURE, max_tokens=config.MAX_TOKENS_PER_RESPONSE):
    """根据模型名称调用相应的API，并传递 Base URL"""
    api_provider = None
    api_key = None
    secret_key = None # 用于百度等
    base_url = None

    # 判断API供应商并获取配置
    # (简化版，你需要为每个供应商添加逻辑)
    if model_name.startswith("gpt"):
        api_provider = "openai"
        api_key = config.OPENAI_API_KEY
        base_url = config.OPENAI_BASE_URL
    elif "claude" in model_name:
        api_provider = "anthropic"
        api_key = config.ANTHROPIC_API_KEY
        base_url = config.ANTHROPIC_BASE_URL
        print(f"模型 {model_name} (Anthropic) 的API调用暂未完全实现。")
        return None # 暂不实现
    elif "gemini" in model_name:
        api_provider = "google"
        api_key = config.GOOGLE_API_KEY
        base_url = config.GOOGLE_BASE_URL # 可能未使用
        print(f"模型 {model_name} (Google) 的API调用暂未完全实现。")
        return None # 暂不实现
    elif model_name.startswith("glm"): # 示例判断智谱模型
         api_provider = "zhipuai"
         api_key = config.ZHIPUAI_API_KEY
         base_url = config.ZHIPUAI_BASE_URL
         print(f"模型 {model_name} (智谱AI) 的API调用暂未完全实现。")
         return None # 暂不实现
    elif model_name.startswith("ernie"): # 示例判断文心模型
         api_provider = "baidu"
         api_key = config.BAIDU_API_KEY
         secret_key = config.BAIDU_SECRET_KEY
         base_url = config.BAIDU_BASE_URL
         print(f"模型 {model_name} (百度文心) 的API调用暂未完全实现。")
         return None # 暂不实现
    # --- 为 Llama 3 和其他开源模型添加逻辑 ---
    # 例如，如果通过像 Anyscale, Together AI, or a local server (Ollama/vLLM) 的 OpenAI 兼容接口访问
    # Llama 3 模型名称可能需要映射，并且你需要设置对应的 Base URL 和 API Key
    elif "Llama-3" in model_name or "Qwen2" in model_name or "DeepSeek" in model_name:
        # 假设这些模型通过 OpenAI 兼容接口访问
        # 你需要在 .env 中设置相应的 BASE_URL 和 API_KEY
        # 例如 OPENAI_BASE_URL="http://localhost:11434/v1" for Ollama
        # API Key 可能对于本地部署是 "ollama" 或其他特定值，或从服务商获取
        api_provider = "openai_compatible_opensource" # 自定义一个名字
        api_key = config.OPENAI_API_KEY # 复用 OpenAI Key 配置或单独配置
        base_url = config.OPENAI_BASE_URL # 复用 OpenAI Base URL 配置或单独配置
        print(f"尝试通过 OpenAI 兼容接口调用开源模型: {model_name} at {base_url}")
        # 注意：你需要确保你的本地服务或API提供商正确配置并运行
        if not base_url:
             print(f"错误：需要为模型 {model_name} 配置 BASE_URL。")
             return None
        # 使用 call_openai_api 进行调用
        api_provider = "openai" # 强制使用openai的调用函数
        # API Key 对于本地服务可能不需要或者是一个固定值，检查你的服务文档


    else:
        print(f"未知的模型供应商: {model_name}")
        return None

    if api_provider != "google" and (not api_key or (isinstance(api_key, str) and api_key.startswith("YOUR_"))): # Google可能只用configure
        # 增加对非字符串或空字符串的检查
        if not isinstance(api_key, str) or api_key.startswith("YOUR_") or not api_key:
             print(f"错误: {api_provider.upper()} API Key 未配置或无效。请检查 config.py 或 .env 文件。")
             return None


    # 调用具体API
    response_text = None
    if api_provider == "openai" or api_provider == "openai_compatible_opensource":
        response_text = call_openai_api(prompt, model_name, api_key, base_url, temperature, max_tokens)
    elif api_provider == "anthropic":
        response_text = call_anthropic_api(prompt, model_name, api_key, base_url, temperature, max_tokens)
    elif api_provider == "google":
        response_text = call_google_api(prompt, model_name, api_key, base_url, temperature, max_tokens)
    elif api_provider == "zhipuai":
         response_text = call_zhipuai_api(prompt, model_name, api_key, base_url, temperature, max_tokens)
    elif api_provider == "baidu":
         response_text = call_baidu_api(prompt, model_name, api_key, secret_key, base_url, temperature, max_tokens)


    # 简单的延迟
    if response_text is not None: # 只有成功调用后才延迟
      time.sleep(config.REQUEST_DELAY)

    return response_text