import os
import sys
import json
from datetime import datetime
from autogen import UserProxyAgent, AssistantAgent
from .agents.autogen_agents import get_specialist_agents, memory
from .config import REPORTS_DIR, LOGS_DIR

class NexusOrchestrator:
    def __init__(self):
        self.specialists = get_specialist_agents()
        self.user_proxy = UserProxyAgent(
            name="User_Proxy",
            system_message="A human admin managing the Nexus AI workflow.",
            code_execution_config=False,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
        )
        self.session_id = datetime.now().strftime("nexus_autogen_%Y%m%d_%H%M%S")
        self.log_path = os.path.join(LOGS_DIR, f"{self.session_id}_trace.log")

    def _log(self, text):
        with open(self.log_path, "a") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {text}\n\n")

    def run(self, goal: str, callback=None):
        self._log(f"SESSION START\nGOAL: {goal}")
        raw_memory = memory.recall(goal)
        memory_summary = (raw_memory[:1000] + "...") if raw_memory and len(raw_memory) > 1000 else raw_memory
        initial_message = f"GOAL: {goal}\n\nMISSION CONTEXT:\n{memory_summary or 'None'}\n\nPlease start by creating the plan."

        pipeline = ["Planner", "Researcher", "Analyst", "Coder", "Critic", "Optimizer", "Validator", "Reporter"]
        current_context = initial_message
        results = {}
        history = []

        for agent_name in pipeline:
            try:
                import time
                time.sleep(2) 
                
                agent = self.specialists[agent_name]
                print(f"[AGENT] Running: {agent_name}...")
                
                if agent_name in ["Optimizer", "Reporter"]:
                    slim_history = [h[:1500] + "..." if len(h) > 1500 else h for h in history]
                    message_for_agent = f"GOAL: {goal}\n\nPROJECT PROGRESS (Slimmed):\n" + "\n".join(slim_history)
                else:
                    message_for_agent = current_context
                
                self.user_proxy.initiate_chat(
                    agent,
                    message=message_for_agent,
                    max_turns=1,
                    silent=True
                )
                
                last_msg = agent.last_message(self.user_proxy)
                output = last_msg["content"]
                results[agent_name] = output
                history.append(f"### WORK FROM {agent_name}:\n{output}\n")
                
                self._log(f"AGENT: {agent_name}\nOUTPUT:\n{output}")
                
                if callback:
                    callback(agent_name, output)

                current_context = f"PREVIOUS WORK ({agent_name}):\n{output}\n\nGOAL: {goal}\n\nPlease proceed with your task."
                
                memory.save_agent_output(self.session_id, {
                    "agent": agent_name,
                    "task": goal,
                    "output": output,
                    "success": True
                })
            except Exception as e:
                if "429" in str(e) or "rate_limit_exceeded" in str(e).lower():
                    error_msg = "Rate limit reached (30 requests per minute). Please wait a moment and try again."
                else:
                    error_msg = f"Error in {agent_name} specialist: {str(e)}"
                
                print(f"[ERROR] {error_msg}")
                memory.save_agent_output(self.session_id, {
                    "agent": agent_name,
                    "task": goal,
                    "output": error_msg,
                    "success": False
                })
                memory.update_task_status(self.session_id, "failed")
                raise RuntimeError(error_msg)

        final_report = results.get("Reporter", "No report generated.")
        report_path = self._save_md_report(goal, final_report, results)
        return report_path, self.session_id

    def _save_md_report(self, goal, report_content, results):
        filename = f"{self.session_id}_report.md"
        path = os.path.join(REPORTS_DIR, filename)

        md = f"# NEXUS AI - AutoGen Report\n\n"
        md += f"**Session:** {self.session_id}\n"
        md += f"**Goal:** {goal}\n\n"
        md += "---\n\n"
        md += report_content
        md += "\n\n---\n\n## Execution Log\n\n"
        for agent, _ in results.items():
            md += f"- [DONE] {agent} completed.\n"

        with open(path, "w") as f:
            f.write(md)
        return path

if __name__ == "__main__":
    orchestrator = NexusOrchestrator()
    goal = sys.argv[1] if len(sys.argv) > 1 else "Plan a tech startup in the AI Education space."
    orchestrator.run(goal)
