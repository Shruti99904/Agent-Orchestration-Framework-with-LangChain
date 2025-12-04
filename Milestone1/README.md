# 🌟 LangChain + Google Gemini — Milestone 1

This is a small, beginner-friendly project where I experimented with **LangChain** using **Google Gemini** as the LLM.  
The goal of this milestone is just to understand the basics — nothing too fancy — but enough to get comfortable with how LangChain works.

In this first milestone, I built:

- ✔️ A simple explanation demo using **PromptTemplate + LLMChain**
- ✔️ Two basic tools (a greeting tool and a weather tool)
- ✔️ A **Zero-Shot ReAct Agent** that decides when to use these tools
- ✔️ A small **console REPL** so I can chat with the agent directly

> ⚠️ **Note:**  
This project still uses the older “classic” LangChain APIs like `LLMChain`, `initialize_agent`, and `ConversationBufferMemory`.  
They’re easy to learn but raise some deprecation warnings — which is fine for this milestone.  
In Milestone-2, I’ll move to the newer LangChain v1 patterns (Runnables, Agents v2, etc.).

---

## 🚀 Features

- Explain any topic in simple words using a prompt + LLM
- A friendly greeting tool
- A lightweight weather tool (using the free `wttr.in` API)
- A Zero-Shot ReAct agent that automatically picks the right tool
- Memory support using `ConversationBufferMemory`
- A simple console interface to interact with the agent
