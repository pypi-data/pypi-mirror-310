# fridaylabs/__init__.py
from .client import FridayLabsClient
from .endpoints.chat import Chat

__all__ = ['FridayLabsClient', 'Chat']