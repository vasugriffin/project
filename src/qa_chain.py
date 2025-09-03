# qa_chain.py
import os
import requests

# Load API key from environment variable
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/v1/chat/completions"  # Verify endpoint in Perplexity docs

def get_bot_response(user_input: str) -> str:
    """Handles conversation with Perplexity API with a mock fallback."""
    
    # Default mock response
    mock_reply = f"[MOCK RESPONSE] You said: {user_input}"

    if not PERPLEXITY_API_KEY:
        print("Warning: PERPLEXITY_API_KEY not set. Returning mock reply.")
        return mock_reply

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "pplx-7b-chat",
        "messages": [{"role": "user", "content": user_input}]
    }

    try:
        response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code != 200:
            print(f"Perplexity API error {response.status_code}: {response.text}")
            return mock_reply

        result = response.json()
        # Safely extract the reply
        reply = result.get("choices", [{}])[0].get("message", {}).get("content")
        if not reply:
            return mock_reply
        return reply

    except Exception as e:
        print(f"Exception while calling Perplexity API: {e}")
        return mock_reply
