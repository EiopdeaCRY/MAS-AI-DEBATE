# src/debate_manager.py
"""
DebateManager 模块
------------------
管理整个多智能体辩论流程：
1. 初始化正反方智能体和裁判智能体
2. 多轮生成辩论发言
3. 裁判总结和评价
"""

from .agents import DebateAgent, JudgeAgent
from .llm_api import call_llm

class DebateManager:
    def __init__(self, topic, pro_stance="支持", con_stance="反对"):
        """
        初始化 DebateManager

        参数:
            topic: str, 辩题
            pro_stance: str, 正方立场
            con_stance: str, 反方立场
        """
        self.topic = topic

        # 初始化正方智能体
        self.pro_agent = DebateAgent(
            role="正方",
            llm=call_llm,    # 必须传 LLM 接口
            stance=pro_stance
        )

        # 初始化反方智能体
        self.con_agent = DebateAgent(
            role="反方",
            llm=call_llm,    # 必须传 LLM 接口
            stance=con_stance
        )

        # 初始化裁判智能体
        self.judge = JudgeAgent(llm=call_llm)

    def run_debate(self, rounds=3, free_debate_rounds=0, context_rounds=1):
        """
        运行多轮辩论

        参数:
            rounds: int, 常规辩论轮数
            free_debate_rounds: int, 自由辩论轮数（0表示不进行自由辩论）
            context_rounds: int, 保留的上下文轮数（1-2轮）

        返回:
            tuple (pro_transcript, con_transcript, judge_summary)
        """
        pro_transcript = ""
        con_transcript = ""

        # 存储最近几轮的发言
        recent_pro_msgs = []
        recent_con_msgs = []
        
        # 常规辩论
        for i in range(1, rounds + 1):
            # 正方发言 - 只传递反方最近context_rounds轮发言
            opponent_for_pro = self._get_recent_context(recent_con_msgs, context_rounds)
            pro_msg = self.pro_agent.respond(self.topic, opponent_for_pro)
            pro_transcript += f"常规轮{i} 正方: {pro_msg}\n"
            recent_pro_msgs.append(pro_msg)
            
            # 只保留最近context_rounds轮
            if len(recent_pro_msgs) > context_rounds:
                recent_pro_msgs = recent_pro_msgs[-context_rounds:]

            # 反方发言 - 只传递正方最近context_rounds轮发言
            opponent_for_con = self._get_recent_context(recent_pro_msgs, context_rounds)
            con_msg = self.con_agent.respond(self.topic, opponent_for_con)
            con_transcript += f"常规轮{i} 反方: {con_msg}\n"
            recent_con_msgs.append(con_msg)
            
            # 只保留最近context_rounds轮
            if len(recent_con_msgs) > context_rounds:
                recent_con_msgs = recent_con_msgs[-context_rounds:]

        # 自由辩论
        if free_debate_rounds > 0:
            pro_transcript += "\n=== 自由辩论 ===\n"
            con_transcript += "\n=== 自由辩论 ===\n"
            
            # 使用最近一轮发言作为自由辩论的起点
            last_pro_argument = recent_pro_msgs[-1] if recent_pro_msgs else "暂无观点"
            last_con_argument = recent_con_msgs[-1] if recent_con_msgs else "暂无观点"
            
            for i in range(1, free_debate_rounds + 1):
                # 正方基于反方观点提问
                pro_question = self.pro_agent.ask_question(self.topic, last_con_argument)
                pro_transcript += f"自由轮{i} 正方提问: {pro_question}\n"
                
                # 反方回答正方的问题
                con_answer = self.con_agent.answer_question(self.topic, pro_question)
                con_transcript += f"自由轮{i} 反方回答: {con_answer}\n"
                last_con_argument = con_answer  # 更新反方观点
                
                # 反方基于正方观点提问
                con_question = self.con_agent.ask_question(self.topic, last_pro_argument)
                con_transcript += f"自由轮{i} 反方提问: {con_question}\n"
                
                # 正方回答反方的问题
                pro_answer = self.pro_agent.answer_question(self.topic, con_question)
                pro_transcript += f"自由轮{i} 正方回答: {pro_answer}\n"
                last_pro_argument = pro_answer  # 更新正方观点

        # 裁判评判 - 优化：如果transcript太长，只传递摘要
        judge_summary = self._optimized_judge_evaluate(pro_transcript, con_transcript)

        # 打印输出
        print("=== 辩论过程 ===")
        print(pro_transcript)
        print(con_transcript)
        print("=== 裁判总结 ===")
        print(judge_summary)

        return pro_transcript, con_transcript, judge_summary

    def _get_recent_context(self, messages, context_rounds):
        """获取最近context_rounds轮的发言上下文"""
        if not messages:
            return None
        # 返回最近几轮的发言，用换行符分隔
        recent = messages[-context_rounds:] if len(messages) >= context_rounds else messages
        return "\n".join(recent)
    
    def _optimized_judge_evaluate(self, pro_transcript, con_transcript):
        """优化裁判评估，如果transcript太长则创建摘要"""
        # 如果transcript不太长，直接使用完整版本
        total_length = len(pro_transcript) + len(con_transcript)
        if total_length < 3000:  # 约1000 tokens
            return self.judge.evaluate(self.topic, pro_transcript, con_transcript)
        
        # 如果太长，创建摘要
        print(f"提示：辩论记录较长({total_length}字符)，正在创建摘要供裁判评估...")
        
        # 简单摘要：只取每轮的前一部分
        pro_summary = self._create_summary(pro_transcript, max_lines=10)
        con_summary = self._create_summary(con_transcript, max_lines=10)
        
        return self.judge.evaluate(self.topic, pro_summary, con_summary)
    
    def _create_summary(self, transcript, max_lines=10):
        """创建transcript的摘要"""
        lines = transcript.split('\n')
        summary_lines = []
        
        for line in lines:
            if not line.strip():
                continue
                
            # 如果是重要行（包含发言内容）
            if '正方:' in line or '反方:' in line or '提问:' in line or '回答:' in line:
                # 提取主要内容
                if ':' in line:
                    prefix, content = line.split(':', 1)
                    # 限制内容长度
                    if len(content) > 150:
                        content = content[:150] + "..."
                    summary_lines.append(f"{prefix}:{content}")
                else:
                    # 限制行长度
                    if len(line) > 150:
                        line = line[:150] + "..."
                    summary_lines.append(line)
            
            # 达到最大行数限制
            if len(summary_lines) >= max_lines:
                break
        
        return "\n".join(summary_lines)
