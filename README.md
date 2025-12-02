# Debate-MAS: Automatic Multi-Agent Debate System

This repository provides a lightweight Multi-Agent System (MAS) that automatically conducts a full debate given a topic. 
You only need to input:

- A debate topic  
- The stance of Agent Pro (supporting)  
- The stance of Agent Con (opposing)

The system will automatically:
1. Generate arguments  
2. Conduct multi-round debate  
3. Produce summaries  
4. Output a combined debate transcript

---

## ✨ Features

- Two-agent debate framework (Pro vs Con)  
- Modular and easy to extend  
- **Designed for DeepSeek framework** (LLM API integration)  
- LLM-agnostic (supports OpenAI, Anthropic, local LLMs…)  
- Multi-round argument exchange  
- Clear architecture flow similar to werewolf-style MAS pipelines  
- **Free debate / interactive questioning**: agents can challenge each other’s logic and ask/answer questions, not just make statements

---

## 🧩 Architecture Overview

See [`architecture_flow.md`](architecture_flow.md).

---

## 🚀 Quick Start

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Run the demo**:

```bash
python -m examples.run_demo
```

> ⚠️ Note: You need to use `python -m examples.run_demo` to run this Debate MAS.  
> Other methods (like `python examples/run_demo.py`) may cause import errors.

---

## 💡 Free Debate / Interactive Mode

- Each round includes:
  1. **Statement Phase**: agents present arguments supporting their stance and can rebut opponent’s points  
  2. **Question Phase**: agents can ask 1-2 questions to challenge or clarify opponent’s argument  
- The system keeps track of all statements and Q&A exchanges in the transcript  
- Judge evaluates both the quality of arguments and the question-answer interactions  
- This makes the debate more realistic and closer to human-style interactions

---

## 📌 Notes

- Ensure you have a valid DeepSeek API key (DPI) set in your environment variables before running.  
- Both agents and the judge will respond **in Chinese only**.  
- The system strictly respects stance; Proponent and Opponent will not switch viewpoints.  
- Multi-round debate transcript will be saved for review.  
- **Recommended to use DeepSeek LLM framework for best performance and compatibility.**

