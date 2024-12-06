# fridaylabs/__init__.py

from .client import FridayLabsClient
from .endpoints.chat import Chat
# Add the following line if you want to expose the chat module
from .endpoints import chat
