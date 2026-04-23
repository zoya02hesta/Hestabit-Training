import autogen
import json
import re
import concurrent.futures
from orchestrator.planner import get_orchestrator
from agents.worker_agent import get_worker_agent
from agents.reflection_agent import get_reflection_agent
from agents.validator import get_validator_agent

def print_execution_tree(query, tasks=None, worker_results=None, reflection=None, validated=False):
    print("\n" + "="*60)
    print(" NEXUS EXECUTION TREE")
    print("="*60)
    print(f" [Query]: \"{query}\"")
    
    if tasks:
        print("└── [Orchestrator]: Task Decomposed")
        for i, task in enumerate(tasks, start=1):
            if isinstance(worker_results, list):
                status = "DONE" if len(worker_results) >= i else "PENDING"
            else:
                status = "DONE" if worker_results else "PENDING"
            print(f"    {'│' if i < len(tasks) else ' '}   ├── {status} [Worker {i}]: {task[:60]}...")
            
    if reflection:
        print("└── [Reflection]: Synthesizing Worker Outputs...")
        
    if validated:
        print("└── [Validator]: Final Verification Complete.")
    print("="*60 + "\n")

def run_worker(index, task, user_proxy):
    worker = get_worker_agent(index)
    user_proxy.initiate_chat(
        worker,
        message=f"YOU ARE WORKER {index}.\nYOUR STRICT ASSIGNMENT: {task}\nDO NOT solve anything else outside of this specific assignment.",
        max_turns=1,
        silent=True
    )
    return index, worker.last_message(user_proxy)["content"]

def main():
    print("Initializing Day 2 Architecture...")
    orchestrator = get_orchestrator()
    reflection = get_reflection_agent()
    validator = get_validator_agent()
    
    user_proxy = autogen.UserProxyAgent(
        name="User_Proxy",
        system_message="A human admin executing the DAG timeline.",
        code_execution_config=False,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
    )
    
    query = input("\n[Terminal Input] Enter your query: ")
    print_execution_tree(query)
    
    print("--- STEP 1: ORCHESTRATION ---")
    user_proxy.initiate_chat(
        orchestrator,
        message=f"Take this query and break it down into 2 distinct tasks for Workers: '{query}'",
        max_turns=1
    )
    task_plan_raw = orchestrator.last_message(user_proxy)["content"]
    json_string = re.sub(r'```json\n|```', '', task_plan_raw).strip()
    
    try:
        task_list = json.loads(json_string)
        print_execution_tree(query, tasks=task_list)
    except json.JSONDecodeError:
        print("\n[ERROR] Orchestrator did not return valid JSON.")
        return

    print("--- STEP 2: DYNAMIC PARALLEL WORKERS ---")
    print("Agent processes started in parallel... please wait.")
    worker_outputs = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(task_list)) as executor:
        futures = {executor.submit(run_worker, i, task, user_proxy): i for i, task in enumerate(task_list, start=1)}
        
        for future in concurrent.futures.as_completed(futures):
            idx, res = future.result()
            worker_outputs[idx] = res
            
    completed_indices = sorted(worker_outputs.keys())
    print_execution_tree(query, tasks=task_list, worker_results=[worker_outputs[i] for i in completed_indices])

    compiled_worker_output = ""
    for i in sorted(worker_outputs.keys()):
        compiled_worker_output += f"\nWorker {i} Results:\n{worker_outputs[i]}\n"

    print("--- STEP 3: REFLECTION ---")
    user_proxy.initiate_chat(
        reflection,
        message=f"Synthesize and reflect to create a cohesive answer:\n{compiled_worker_output}",
        max_turns=1,
        silent=True
    )
    reflection_output = reflection.last_message(user_proxy)["content"]
    print_execution_tree(query, tasks=task_list, worker_results=True, reflection=reflection_output)

    print("--- STEP 4: VALIDATOR ---")
    user_proxy.initiate_chat(
        validator,
        message=f"Verify this final synthesized draft for: '{query}'. Provide final output and TERMINATE.\n\nDraft:\n{reflection_output}",
        max_turns=1,
        silent=True
    )
    print_execution_tree(query, tasks=task_list, worker_results=True, reflection=reflection_output, validated=True)
    
    print("\n[DAG Pipeline Complete!]")

if __name__ == "__main__":
    main()
