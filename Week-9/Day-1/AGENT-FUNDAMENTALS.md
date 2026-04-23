# Agent Fundamentals: Day 1

## What is an AI agent?
An AI agent is a system capable of perceiving its environment, reasoning about it using an underlying intelligence (usually an LLM), and taking actions to achieve a specific goal. Unlike traditional software that strictly follows pre-programmed logical paths, agents can handle ambiguity and make autonomous decisions to complete tasks.

## Agent vs Chatbot vs Pipeline
*   **Chatbot:** A conversational interface designed primarily to exchange messages with a user. It simply responds to immediate prompts based on its training data or simple RAG, without autonomy or long-term multi-step planning.
*   **Pipeline:** A hardcoded sequence of steps (e.g., Step A -> Step B -> Step C). Data flows through a rigid structure. If an unexpected situation arises, a pipeline will fail because it cannot reconsider its execution plan.
*   **Agent:** Autonomous, flexible, and capable of adapting to unexpected situations. It uses tools, reasons about intermediate states, and recursively corrects itself until the objective is accomplished.

## Perception → Reasoning → Action Loop
Agents operate continuously in this loop:
1.  **Perception:** Gathering input from the environment (e.g., observing user messages, reading API responses, monitoring logs).
2.  **Reasoning:** Analyzing the perceived data to decide on the best strategy (e.g., using chain-of-thought, decomposing a larger task).
3.  **Action:** Executing a decision (e.g., making an API call, running code, sending a message to a human or another agent).

## Message Protocol Systems
In a multi-agent system, agents interact via highly structured message passing. Messages typically include meta-data (sender, intent, context) along with payloads. This decouples the processing of information; agents handle only what they are designed for. This architecture is similar to microservices, but they are governed by conversational semantics and prompt boundaries rather than strict, static API schemas.

## Agent Architecture
Modern agents follow an architecture extending far beyond a plain LLM:
*   **Core Model:** The reasoning brain (e.g., Phi-3, Mistral, TinyLlama, Qwen).
*   **Memory:** Short-term (context window, recent messages memory window) and Long-term (vector databases like FAISS, relational DBs like SQLite).
*   **Tools/Plugins:** Execution environments allowing agents to read files, search the web, execute code, etc.
*   **Planner/Orchestrator:** High-level supervision to coordinate sub-agents or complex multi-step workflows.

## ReAct Pattern (Reason + Act)
ReAct is a prompt engineering paradigm that forces an LLM to generate alternating *thoughts* (reasoning) and *actions* (tool uses or observable behaviors).
*   **Thought:** "I need to find the user's latest file to summarize."
*   **Action:** `search_directory("/home/user/files")`
*   **Observation:** List of files...
*   **Thought:** "The most recent is document.txt. I will summarize it."
This grounds the LLM into real-world observations instead of hallucinated solutions.

## LLM as a Tool Executor
Instead of merely generating conversational text, the LLM is given access to a schema of callable functions (e.g., `get_weather(location)`). The LLM processes the user prompt, determines the required arguments, and outputs a structured payload to invoke the tool. The agentic framework intercepts this, runs the actual Python/API code, and returns the execution result to the LLM.

## System Prompts for Agents
System prompts act as the "DNA" and rules of engagement for an agent. They define:
*   **Role and Identity:** (e.g., "You are an expert strict research assistant.").
*   **Constraints:** (e.g., "Never write code, only summarize text.").
*   **Output Format:** (e.g., "Always output valid JSON.").
*   **Workflow rules:** (e.g., "If you fail to find information, explicitly alert the human.").

## Role Isolation
Strict job separation is crucial in multi-agent designs. A single agent trying to perform research, code execution, and summarizing simultaneously often suffers from prompt confusion or loses context. Role isolation assigns highly specific, narrow responsibilities to individual agents. For instance, the Research Agent gathers facts, but the Summarizer Agent *only* distills text. This promotes modularity, robustness, and an easily debugged cognitive workflow.
