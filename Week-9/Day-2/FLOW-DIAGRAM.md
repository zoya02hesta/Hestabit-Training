# Directed Acyclic Graph (DAG) Agent Execution Flow

This diagram outlines how the Orchestrator distributes tasks and how parallel execution is folded back into a sequential loop for Reflection and Validation.

```mermaid
graph TD
    A[User Query] --> B(Orchestrator/Planner);
    
    B -->|Generates Task Breakdown| C{Parallel Splitting};
    
    C -->|Task 1| W1[Worker Agent 1];
    C -->|Task 2| W2[Worker Agent 2];
    C -->|Task N| WN[Worker Agent N];
    
    W1 --> D[Context Assembly];
    W2 --> D;
    WN --> D;
    
    D --> E(Reflection Agent);
    
    E -->|Synthesized Draft| F(Validator Agent);
    
    F -->|Validation Fails| E;
    F -->|Validation Passes| G[Final Answer];

    
```

### Explaining the Steps

1. **Planner**: Decides *what* needs to be done. It isolates dependencies so workers don't block each other.
2. **Workers**: Operate in an isolated context. They rely strictly on their individual system prompts and the sub-task assigned to them without awareness of the overarching problem.
3. **Reflection**: The "Merge" phase. It takes disparate JSONs, strings, and texts from all workers and synthesizes them into a unified draft. 
4. **Validator**: Applies hard constraints. If the query strictly asked for Python code and the reflection outputs Java, the Validator kicks it back. Once correct, it terminates.
