import autogen
from agents.research_agent import get_research_agent
from agents.summarizer_agent import get_summarizer_agent
from agents.answer_agent import get_answer_agent

def main():
    print("Initializing Agents...")
    research_agent = get_research_agent()
    summarizer_agent = get_summarizer_agent()
    answer_agent = get_answer_agent()
    
    # The proxy agent acts on behalf of the user to trigger the pipeline
    user_proxy = autogen.UserProxyAgent(
        name="User_Proxy",
        system_message="A human admin executing the Agent pipeline.",
        code_execution_config=False,
        human_input_mode="NEVER",  # Run autonomously for the test
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"].upper()
    )
    
    # Dynamic Terminal Input
    query = input("\n[Terminal Input] Enter your research question for Day 1: ")
    print(f"\n[Processing Query]: {query}\n")

    # Defining the Sequential Chat pipeline
    # User -> Research -> Summarizer -> Answer
    
    chat_sequence = [
        {
            "recipient": research_agent,
            "message": f"Research this topic: {query}",
            "summary_method": "last_msg",
            "max_turns": 1, 
            # We take the raw output and forward it to the next agent
        },
        {
            "recipient": summarizer_agent,
            "message": "Here is the raw research. Please summarize it.",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": answer_agent,
            "message": f"Based on the summary, provide a final, polished answer to the original query: {query}",
            "summary_method": "last_msg",
            "max_turns": 1,
        }
    ]

    print("Starting Sequential Agent Pipeline...")
    
    try:
        # Executing the chat pipeline
        user_proxy.initiate_chats(chat_sequence)
        print("\nPipeline Complete!")
    except Exception as e:
        print(f"\nError running pipeline: {e}")
        print("Note: To run this pipeline, ensure your local Open-Source model (e.g. Ollama) is running on the endpoint defined in agents/config.py")

if __name__ == "__main__":
    main()
