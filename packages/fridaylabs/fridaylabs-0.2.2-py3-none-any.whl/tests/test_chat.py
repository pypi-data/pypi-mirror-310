# tests/test_chat.py

import unittest
from unittest.mock import patch
from fridaylabs import Chat

class TestChat(unittest.TestCase):
    def setUp(self):
        self.chat_client = Chat(api_key='test_api_key', verbose=False)

    @patch('fridaylabs.client.requests.post')
    def test_chat_completion_success(self, mock_post):
        mock_response = unittest.mock.Mock()
        expected_output = {'message': 'Test response'}
        mock_response.json.return_value = expected_output
        mock_response.status_code = 200
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_post.return_value = mock_response

        messages = [{'role': 'user', 'content': 'Hello'}]
        response = self.chat_client.chat_completion('test-model', messages)

        self.assertEqual(response, expected_output)

    # Add more tests for error handling

if __name__ == '__main__':
    unittest.main()
