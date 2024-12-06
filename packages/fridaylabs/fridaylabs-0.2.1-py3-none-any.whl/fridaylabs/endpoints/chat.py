# fridaylabs/endpoints/chat.py

from ..client import FridayLabsClient

class Chat(FridayLabsClient):
    def chat_completion(self, model, messages, temperature=1, max_tokens=256,
                        top_p=1, frequency_penalty=0, presence_penalty=0):
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        return self._send_request('POST', '/chat', payload)
