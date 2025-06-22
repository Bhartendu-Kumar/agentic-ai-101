# agentic-ai-101
Repository for learning Agentic AI

## Table of Contents
- [About This Repository](#about-this-repository)
- [Topics Covered](#topics-covered)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Join on Whatsapp](#join-on-whatsapp)

## About This Repository
Welcome to `agentic-ai-101`! This repository is designed as a hands-on learning resource for understanding and implementing **Agentic AI** concepts, with a strong focus on **Large Language Models (LLMs)**. Whether you're new to the field or looking to deepen your understanding, this guide will walk you through the fundamentals of building intelligent agents powered by LLMs.

We'll explore various aspects, from setting up local LLM environments to crafting sophisticated agentic workflows.

## Topics Covered
This repository aims to cover a range of topics essential for building Agentic AI systems, including but not limited to:

*   **Understanding Large Language Models (LLMs):** Basics of how LLMs work and their capabilities.
*   **Local LLM Setup:** Running LLMs locally using tools like Ollama for experimentation and privacy.
    *   *Example:* See `using_llms/local/ollama/ollama_syntax.json` for basic Ollama API interaction examples.
*   **Prompt Engineering:** Techniques for effectively communicating with LLMs.
*   **Agentic Workflows:** Designing and implementing systems where LLMs act as intelligent agents, performing tasks, making decisions, and interacting with tools.
*   **Tool Use and Integration:** Enabling LLMs to interact with external APIs and services.
*   **Memory and State Management:** Giving agents the ability to remember past interactions.
*   **Evaluation and Testing:** Strategies for assessing agent performance.

## Project Structure
The repository is organized to guide you through different aspects of Agentic AI:

```
.
├── README.md
├── using_llms/
│   ├── local/
│   │   └── ollama/
│   │       └── ollama_syntax.json  # Example JSON structure for Ollama 
│   │       └── ollama_1.py    # Python script to interact with Ollama API
│   │       ...
│   │       └── ollama_3.py    # Python script to interact with Ollama API
│   │       
│   ├── cloud/
│   │   └── chutes/
│   │       └── chutes.py  # basic script to interact with Chutes LLM
│   └── ...                         # Other LLM examples
│   
├── tool_use/
│   └── RAG                        # Examples of tool use with RAG
│       └── ...
│   └── search/                    # Examples of tool use with search
│       └── ...
│   └── memory/                    # Examples of memory management
│       └── ...
│   └── ...                         # Other tool use examples
│       
├── agents/
│   └── ...                         # Examples of agent implementations
└── PROJECTS/
│   ├── chatbots/                  # Examples of chatbot workflows
    └── ...                         # Examples of agent implementations
```

*   `using_llms/`: Contains examples and scripts for interacting with various LLMs, both local and cloud-based.
    *   `local/`: Focuses on running LLMs on your local machine.
        *   `ollama/`: Specific examples and configurations for using Ollama.
*   `agents/`: Will house different agent implementations, demonstrating various agentic patterns and frameworks.

## Getting Started
To get started with the examples in this repository:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/agentic-ai-101.git
    cd agentic-ai-101
    ```
2.  **Install necessary dependencies:** (Specific instructions will be added as code examples are populated)
    *   For Ollama examples, you'll need to install Ollama: https://ollama.com/download
    *   Python dependencies will be listed in `requirements.txt` within specific subdirectories.

## Join on Whatsapp
[Join the WhatsApp Group](https://chat.whatsapp.com/F0Chqhp8kwPKRSEMRmkjvG)

[![WhatsApp Group Invite](group_invite.png)](https://chat.whatsapp.com/F0Chqhp8kwPKRSEMRmkjvG)