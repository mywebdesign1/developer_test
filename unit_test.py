import unittest
from unittest.mock import patch, MagicMock
from sync_data import fetch_data, store_data, SessionLocal

class TestSyncData(unittest.TestCase):

    @patch('sync_data.requests.post')
    def test_fetch_data(self, mock_post):
        mock_response = MagicMock()
        expected_data = {
            "data": {
                "pools": [
                    {"id": "1", "token0": {"id": "token0_1"}, "token1": {"id": "token1_1"}},
                    {"id": "2", "token0": {"id": "token0_2"}, "token1": {"id": "token1_2"}}
                ]
            }
        }
        mock_response.status_code = 200
        mock_response.json.return_value = expected_data
        mock_post.return_value = mock_response

        result = fetch_data()
        self.assertEqual(result, expected_data)

    @patch('sync_data.SessionLocal')
    def test_store_data(self, mock_SessionLocal):
        mock_session = MagicMock()
        mock_SessionLocal.return_value = mock_session
        data = {
            "data": {
                "pools": [
                    {"id": "1", "token0": {"id": "token0_1"}, "token1": {"id": "token1_1"}},
                    {"id": "2", "token0": {"id": "token0_2"}, "token1": {"id": "token1_2"}}
                ]
            }
        }

        store_data(data)
        self.assertTrue(mock_session.commit.called)

if __name__ == '__main__':
    unittest.main()
