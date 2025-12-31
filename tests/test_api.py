import unittest
import sys
import os
from unittest.mock import patch, Mock

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.crypto_api import get_crypto_data, get_multiple_cryptos

class TestCryptoAPI(unittest.TestCase):
    
    @patch('utils.crypto_api.requests.get')
    def test_get_crypto_data_success(self, mock_get):
        """Test récupération réussie des données crypto"""
        # Mock de la réponse API
        mock_response = Mock()
        mock_response.json.return_value = {
            'bitcoin': {
                'usd': 45000.50,
                'usd_24h_change': 2.34
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_crypto_data('bitcoin')
        
        self.assertEqual(result['name'], 'Bitcoin')
        self.assertEqual(result['price'], 45000.50)
        self.assertEqual(result['change'], 2.34)
    
    @patch('utils.crypto_api.requests.get')
    def test_get_crypto_data_api_error(self, mock_get):
        """Test gestion d'erreur API"""
        mock_get.side_effect = Exception("API Error")
        
        result = get_crypto_data('bitcoin')
        
        self.assertEqual(result['name'], 'Bitcoin (Erreur)')
        self.assertEqual(result['price'], 0)
        self.assertEqual(result['change'], 0)
    
    @patch('utils.crypto_api.requests.get')
    def test_get_crypto_data_crypto_not_found(self, mock_get):
        """Test crypto non trouvée"""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_crypto_data('unknown_crypto')
        
        self.assertEqual(result['name'], 'Unknown_crypto (Erreur)')
        self.assertEqual(result['price'], 0)
        self.assertEqual(result['change'], 0)
    
    @patch('utils.crypto_api.requests.get')
    def test_get_multiple_cryptos_success(self, mock_get):
        """Test récupération de plusieurs cryptos"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'bitcoin': {'usd': 45000, 'usd_24h_change': 2.34},
            'ethereum': {'usd': 3000, 'usd_24h_change': -1.23}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_multiple_cryptos(['bitcoin', 'ethereum'])
        
        self.assertIn('bitcoin', result)
        self.assertIn('ethereum', result)
        self.assertEqual(result['bitcoin']['usd'], 45000)
        self.assertEqual(result['ethereum']['usd'], 3000)
    
    @patch('utils.crypto_api.requests.get')
    def test_get_multiple_cryptos_error(self, mock_get):
        """Test erreur lors de la récupération de plusieurs cryptos"""
        mock_get.side_effect = Exception("API Error")
        
        result = get_multiple_cryptos(['bitcoin', 'ethereum'])
        
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()