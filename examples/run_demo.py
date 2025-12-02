# examples/run_demo.py
"""
交互式运行 MAS 辩论示例
----------------------
运行时可以输入：
1. 辩题
2. 常规辩论轮数
3. 自由辩论轮数
4. 上下文保留轮数
"""

from src.debate_manager import DebateManager

def main():
    print("=== 欢迎使用多智能体辩论系统 ===")

    # 输入辩题
    topic = input("请输入辩题（例如：AI 是否应该替代老师？）： ").strip()
    if not topic:
        topic = "AI 是否应该替代老师？"  # 默认辩题

    # 输入常规辩论轮数
    rounds_input = input("请输入常规辩论轮数（默认 3 轮）： ").strip()
    try:
        rounds = int(rounds_input)
        if rounds <= 0:
            rounds = 3
    except:
        rounds = 3

    # 输入自由辩论轮数
    free_rounds_input = input("请输入自由辩论轮数（默认 0 轮，不进行自由辩论）： ").strip()
    try:
        free_debate_rounds = int(free_rounds_input)
        if free_debate_rounds < 0:
            free_debate_rounds = 0
    except:
        free_debate_rounds = 0

    # 输入上下文保留轮数
    context_input = input("请输入上下文保留轮数（默认 1 轮，建议 1-2 轮）： ").strip()
    try:
        context_rounds = int(context_input)
        if context_rounds < 1:
            context_rounds = 1
        elif context_rounds > 5:
            context_rounds = 5
    except:
        context_rounds = 1

    print(f"\n=== 开始辩论 ===\n辩题：{topic}\n常规轮数：{rounds}\n自由辩论轮数：{free_debate_rounds}\n上下文保留轮数：{context_rounds}\n")

    # 初始化 DebateManager
    manager = DebateManager(topic)

    # 运行辩论
    manager.run_debate(rounds=rounds, free_debate_rounds=free_debate_rounds, context_rounds=context_rounds)

if __name__ == "__main__":
    main()
