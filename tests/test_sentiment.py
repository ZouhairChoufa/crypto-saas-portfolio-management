import unittest
import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.sentiment import analyze_sentiment, get_market_sentiment, get_sentiment_color

class TestSentiment(unittest.TestCase):
    
    def test_analyze_sentiment_very_positive(self):
        """Test sentiment très positif"""
        result = analyze_sentiment(10.5)
        self.assertEqual(result, 'Très Positif')
    
    def test_analyze_sentiment_positive(self):
        """Test sentiment positif"""
        result = analyze_sentiment(3.2)
        self.assertEqual(result, 'Positif')
    
    def test_analyze_sentiment_neutral(self):
        """Test sentiment neutre"""
        result = analyze_sentiment(0.5)
        self.assertEqual(result, 'Neutre')
    
    def test_analyze_sentiment_negative(self):
        """Test sentiment négatif"""
        result = analyze_sentiment(-3.2)
        self.assertEqual(result, 'Négatif')
    
    def test_analyze_sentiment_very_negative(self):
        """Test sentiment très négatif"""
        result = analyze_sentiment(-8.5)
        self.assertEqual(result, 'Très Négatif')
    
    def test_get_market_sentiment_structure(self):
        """Test la structure du sentiment de marché"""
        result = get_market_sentiment()
        self.assertIn('sentiment', result)
        self.assertIn('score', result)
        self.assertIn('description', result)
        self.assertIsInstance(result['score'], int)
    
    def test_get_sentiment_color(self):
        """Test les couleurs de sentiment"""
        self.assertEqual(get_sentiment_color('Très Positif'), 'text-green-500')
        self.assertEqual(get_sentiment_color('Positif'), 'text-green-400')
        self.assertEqual(get_sentiment_color('Neutre'), 'text-gray-400')
        self.assertEqual(get_sentiment_color('Négatif'), 'text-red-400')
        self.assertEqual(get_sentiment_color('Très Négatif'), 'text-red-500')
        self.assertEqual(get_sentiment_color('Inconnu'), 'text-gray-400')

if __name__ == '__main__':
    unittest.main()