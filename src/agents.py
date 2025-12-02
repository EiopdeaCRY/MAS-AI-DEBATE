# src/agents.py
"""
Agents 模块
-------------
包含 DebateAgent（正反方智能体）和 JudgeAgent（裁判智能体）

改进点：
1. 输出中文，避免中英文混杂
2. 正反方严格坚持自己的立场
3. Prompt 明确提示 LLM 不要偏离立场
"""

from .llm_api import call_llm

class DebateAgent:
    def __init__(self, role, llm, stance=None):
        """
        初始化辩论智能体

        参数:
            role: str, 角色名，例如 "正方" 或 "反方"
            llm: 函数, 用于生成文本的 LLM 接口 (call_llm)
            stance: str, 智能体立场，例如 "支持 AI 教学"
        """
        self.role = role
        self.llm = llm
        self.stance = stance

    def respond(self, topic, opponent_msg=None):
        """
        生成辩论发言

        参数:
            topic: str, 议题
            opponent_msg: str, 对手上一轮发言

        返回:
            str, 智能体生成的发言
        """
        # 中文提示，明确立场
        prompt = f"""
你是辩论中的 {self.role}。
议题: {topic}
你的立场: {self.stance}

请根据你的立场回答，绝对不要偏离你的立场。
对手观点：
{opponent_msg}

请用中文简明、有力、逻辑清晰地表达你的观点。
"""

        # 调用 LLM 生成文本
        return self.llm(prompt)

    def ask_question(self, topic, opponent_argument):
        """
        基于对方观点提出问题，寻找逻辑漏洞

        参数:
            topic: str, 议题
            opponent_argument: str, 对方的观点或论证

        返回:
            str, 提出的问题
        """
        prompt = f"""
你是辩论中的 {self.role}。
议题: {topic}
你的立场: {self.stance}

对方观点：
{opponent_argument}

请基于对方观点，提出一个尖锐的问题来挑战对方的逻辑。
重点寻找对方论证中的漏洞、矛盾或不一致之处。
你的问题应该：
1. 直接针对对方观点的弱点
2. 揭示逻辑上的问题
3. 迫使对方不得不认真回应
4. 用中文提问
"""
        return self.llm(prompt)

    def answer_question(self, topic, question):
        """
        回答对方提出的问题

        参数:
            topic: str, 议题
            question: str, 对方提出的问题

        返回:
            str, 对问题的回答
        """
        prompt = f"""
你是辩论中的 {self.role}。
议题: {topic}
你的立场: {self.stance}

对方提出的问题：
{question}

请用中文回答这个问题，同时：
1. 维护你的立场
2. 反驳问题中隐含的质疑
3. 保持逻辑一致性
4. 如果可能，将问题转化为支持你立场的机会
"""
        return self.llm(prompt)


class JudgeAgent:
    def __init__(self, llm):
        """
        初始化裁判智能体

        参数:
            llm: 函数, 用于生成文本的 LLM 接口 (call_llm)
        """
        self.llm = llm

    def evaluate(self, topic, pro_transcript, con_transcript):
        """
        对辩论进行评判

        参数:
            topic: str, 辩题
            pro_transcript: str, 正方所有发言记录
            con_transcript: str, 反方所有发言记录

        返回:
            str, 裁判总结和评价
        """
        prompt = f"""
你是辩论裁判。

议题: {topic}

正方发言记录:
{pro_transcript}

反方发言记录:
{con_transcript}

请用中文总结双方观点，并给出客观评价。
"""
        return self.llm(prompt)
