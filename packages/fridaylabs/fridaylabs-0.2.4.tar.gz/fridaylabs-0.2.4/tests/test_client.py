# test_fridaylabs.py
from fridaylabs import FridayLabsClient

def test_client_usage():
    """
    Example using the FridayLabsClient class (recommended approach)
    """
    # Initialize the client
    client = FridayLabsClient(api_key="your_api_key", verbose=True)
    
    # Use the chat endpoint through the client
    try:
        response = client.chat.chat_completion(
            model="fridayai",
            messages=[{"role": "user", "content": "Tell me a joke."}],
            temperature=0.7,
            max_tokens=150,
        )
        print("API Response:", response)
    except Exception as e:
        print(f"An error occurred: {e}")

def test_direct_chat():
    """
    Example using the Chat class directly (alternative approach)
    """
    from fridaylabs.endpoints.chat import Chat
    
    # Initialize Chat directly
    chat = Chat(api_key="your_api_key", verbose=True)
    
    try:
        response = chat.chat_completion(
            model="fridayai",
            messages=[{"role": "user", "content": "Tell me a joke."}],
            temperature=0.7,
            max_tokens=150,
        )
        print("API Response:", response)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Testing client usage:")
    test_client_usage()
    
    print("\nTesting direct chat usage:")
    test_direct_chat()