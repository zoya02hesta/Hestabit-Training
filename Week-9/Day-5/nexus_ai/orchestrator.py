import os
import sys
import json
from datetime import datetime
from autogen import UserProxyAgent, AssistantAgent
from .agents.autogen_agents import get_specialist_agents, memory
from .config import llm_config, REPORTS_DIR

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

    def run(self, goal: str, callback=None):
        print(f"\n[INFO] Starting NEXUS AI Pipeline")
        print(f"[GOAL] {goal}\n")

        # 1. Memory recall
        memory_context = memory.recall(goal)
        initial_message = f"GOAL: {goal}\n\nCONTEXT FROM MEMORY:\n{memory_context or 'None'}\n\nPlease start by creating the plan."

        # 2. Sequential Pipeline Execution
        pipeline = ["Planner", "Researcher", "Analyst", "Coder", "Critic", "Optimizer", "Validator", "Reporter"]
        current_context = initial_message
        results = {}

        for agent_name in pipeline:
            agent = self.specialists[agent_name]
            print(f"[AGENT] Running: {agent_name}...")
            
            # Use initiate_chat to get the agent's output
            chat_status = self.user_proxy.initiate_chat(
                agent,
                message=current_context,
                max_turns=1,
                silent=True
            )
            
            # Extract last message
            output = agent.last_message(self.user_proxy)["content"]
            results[agent_name] = output
            
            # Callback for UI
            if callback:
                callback(agent_name, output)

            # Update context for the next agent
            current_context = f"PREVIOUS WORK ({agent_name}):\n{output}\n\nGOAL: {goal}\n\nPlease proceed with your task."
            
            # Save to Nexus Memory
            memory.save_agent_output(self.session_id, {
                "agent": agent_name,
                "task": goal,
                "output": output,
                "success": True
            })

        # 3. Save Report
        final_report = results.get("Reporter", "No report generated.")
        report_path = self._save_md_report(goal, final_report, results)
        
        print(f"\n[SUCCESS] NEXUS AI Pipeline Complete")
        print(f"[OUTPUT] Report saved: {report_path}")
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
