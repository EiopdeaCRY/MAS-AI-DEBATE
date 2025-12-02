# src/llm_api.py
"""
DeepSeek LLM API 封装模块
-------------------------
这个模块封装了 MAS 系统调用 DeepSeek LLM 的逻辑，
使用 OpenAI SDK 风格接口，返回生成文本。

使用方式：
    from llm_api import call_llm
    text = call_llm("你的提示词")
"""

import os
from openai import OpenAI

# =========================
# 获取 API Key
# 从环境变量 DEEPSEEK_API_KEY 读取
# 这样密钥不会写在代码里，更安全
# =========================
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError(
        "请先在系统环境变量中设置 DEEPSEEK_API_KEY\n"
        "Linux/macOS: export DEEPSEEK_API_KEY='你的密钥'\n"
        "Windows(cmd/PowerShell): set DEEPSEEK_API_KEY=你的密钥"
    )

# =========================
# 初始化 DeepSeek 客户端
# base_url 使用 DeepSeek 官方 API 地址
# =========================
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# =========================
# call_llm: 核心函数
# 参数:
#   prompt: str，给 LLM 的提示词
# 返回:
#   str，LLM 生成的文本
# =========================
def call_llm(prompt):
    """
    调用 DeepSeek LLM API 生成文本
    """
    try:
        # 调用 chat completion 接口
        response = client.chat.completions.create(
            model="deepseek-chat",  # DeepSeek 官方聊天模型
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        # 返回生成的文本
        return response.choices[0].message.content

    except Exception as e:
        # 如果调用 API 出错，抛出异常
        raise Exception(f"DeepSeek API 调用失败: {e}")
