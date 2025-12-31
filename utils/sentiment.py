import random
from typing import Dict

def analyze_sentiment(price_change: float) -> str:
    """
    Analyse le sentiment basé sur la variation de prix
    (Version simplifiée - sera améliorée avec de l'IA plus tard)
    
    Args:
        price_change (float): Variation de prix en pourcentage
    
    Returns:
        str: Sentiment analysé ('Très Positif', 'Positif', 'Neutre', 'Négatif', 'Très Négatif')
    """
    if price_change > 5:
        return 'Très Positif'
    elif price_change > 2:
        return 'Positif'
    elif price_change > -2:
        return 'Neutre'
    elif price_change > -5:
        return 'Négatif'
    else:
        return 'Très Négatif'

def get_market_sentiment() -> Dict:
    """
    Génère un sentiment de marché global
    (Version mock - sera remplacée par une vraie analyse)
    
    Returns:
        Dict: Sentiment du marché avec score et description
    """
    sentiments = [
        {'sentiment': 'Très Positif', 'score': 85, 'description': 'Le marché est très optimiste'},
        {'sentiment': 'Positif', 'score': 70, 'description': 'Tendance haussière observée'},
        {'sentiment': 'Neutre', 'score': 50, 'description': 'Marché stable, pas de tendance claire'},
        {'sentiment': 'Négatif', 'score': 30, 'description': 'Inquiétudes sur le marché'},
        {'sentiment': 'Très Négatif', 'score': 15, 'description': 'Forte baisse, panique du marché'}
    ]
    
    return random.choice(sentiments)

def get_sentiment_color(sentiment: str) -> str:
    """
    Retourne la couleur CSS correspondant au sentiment
    
    Args:
        sentiment (str): Le sentiment analysé
    
    Returns:
        str: Classe CSS de couleur
    """
    color_map = {
        'Très Positif': 'text-green-500',
        'Positif': 'text-green-400',
        'Neutre': 'text-gray-400',
        'Négatif': 'text-red-400',
        'Très Négatif': 'text-red-500'
    }
    
    return color_map.get(sentiment, 'text-gray-400')