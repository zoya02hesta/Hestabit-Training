import time
import re
import groq

def call_groq_with_retry(client, **kwargs):
    """
    Wrapper for client.chat.completions.create with 429 RateLimit handling.
    Parses wait time from Groq's error message.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(**kwargs)
        except groq.RateLimitError as e:
            msg = str(e)
            # Match formats like "6m22.752s" or "42s"
            match = re.search(r"Please try again in ([\d\.ms]+)", msg)
            if match:
                wait_time_str = match.group(1)
                
                # Simple parsing logic
                total_seconds = 0
                
                # Parse minutes
                m_match = re.search(r"(\d+)m", wait_time_str)
                if m_match:
                    total_seconds += int(m_match.group(1)) * 60
                
                # Parse seconds
                s_match = re.search(r"(\d+\.?\d*)s", wait_time_str)
                if s_match:
                    total_seconds += float(s_match.group(1))
                
                if total_seconds == 0: # Default fallback
                    total_seconds = 60
                
                print(f"[Rate Limit] {wait_time_str} wait required. Pausing for {int(total_seconds)}s...")
                time.sleep(total_seconds + 1)
            else:
                wait = (attempt + 1) * 30
                print(f"[Rate Limit] Unknown wait time. Retrying in {wait}s...")
                time.sleep(wait)
    
    # Final attempt let the error raise if retries exhausted
    return client.chat.completions.create(**kwargs)
