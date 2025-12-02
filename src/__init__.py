# src/__init__.py
# 标记 src 目录为包，并统一导入常用类

from .agents import DebateAgent, JudgeAgent
from .debate_manager import DebateManager

__version__ = "0.1"
