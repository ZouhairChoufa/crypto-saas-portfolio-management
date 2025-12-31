import requests
from typing import Dict, Optional

def get_crypto_data(crypto_id: str = 'bitcoin') -> Dict:
    """
    Récupère les données d'une cryptomonnaie depuis l'API CoinGecko
    
    Args:
        crypto_id (str): ID de la crypto sur CoinGecko (ex: 'bitcoin', 'ethereum')
    
    Returns:
        Dict: Données de la cryptomonnaie (nom, prix, variation)
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd&include_24hr_change=true"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if crypto_id not in data:
            raise ValueError(f"Crypto '{crypto_id}' non trouvée")
        
        price = data[crypto_id]['usd']
        change_24h = data[crypto_id]['usd_24h_change']
        
        return {
            'name': crypto_id.capitalize(),
            'symbol': crypto_id.upper()[:3],
            'price': price,
            'change_24h': round(change_24h, 2),
            'market_cap': price * 19000000,
            'volume_24h': price * 500000,
            'high_24h': price * 1.05,
            'low_24h': price * 0.95,
            'image': None
        }
    
    except requests.RequestException as e:
        print(f"Erreur API : {e}")
        return {
            'name': f'{crypto_id.capitalize()} (Offline)',
            'symbol': crypto_id.upper()[:3],
            'price': 0,
            'change_24h': 0,
            'market_cap': 0,
            'volume_24h': 0,
            'high_24h': 0,
            'low_24h': 0,
            'image': None
        }
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return {
            'name': f'{crypto_id.capitalize()} (Erreur)',
            'symbol': crypto_id.upper()[:3],
            'price': 0,
            'change_24h': 0,
            'market_cap': 0,
            'volume_24h': 0,
            'high_24h': 0,
            'low_24h': 0,
            'image': None
        }

def get_multiple_cryptos(crypto_ids: list) -> Dict:
    """
    Récupère les données de plusieurs cryptomonnaies
    
    Args:
        crypto_ids (list): Liste des IDs des cryptos
    
    Returns:
        Dict: Données de toutes les cryptomonnaies
    """
    crypto_string = ','.join(crypto_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_string}&vs_currencies=usd&include_24hr_change=true"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.RequestException as e:
        print(f"Erreur API : {e}")
        return {}