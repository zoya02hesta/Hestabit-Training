def build_chat_prompt(system, user, history):
    prompt = f"<|system|>\n{system}\n"

    for h in history:
        prompt += f"<|user|>\n{h['user']}\n<|assistant|>\n{h['assistant']}\n"

    prompt += f"<|user|>\n{user}\n<|assistant|>\n"

    return prompt