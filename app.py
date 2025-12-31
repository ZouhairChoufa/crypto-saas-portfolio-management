import requests
import random
import os
from flask import Flask, render_template, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import time

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Initialiser l'IA
analyzer = SentimentIntensityAnalyzer()

# Cache simple pour éviter trop de requêtes API
price_cache = {'timestamp': None, 'data': None}
history_cache = {'timestamp': None, 'data': None}
CACHE_DURATION = 10  # 10 secondes pour plus de réactivité
HISTORY_CACHE_DURATION = 300  # 5 minutes pour l'historique

# --- FONCTION NOUVELLE : HISTORIQUE RÉEL ---
def get_real_history(coin_id='bitcoin'):
    """Récupère l'historique réel des prix avec CoinGecko"""
    global history_cache
    
    # Vérifier le cache
    now = datetime.now()
    if history_cache['timestamp'] and (now - history_cache['timestamp']).seconds < HISTORY_CACHE_DURATION:
        return history_cache['data']
    
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': '1',
        'interval': 'hourly'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'prices' in data:
            prices = data['prices']
            historical_data = []
            
            for i, price_point in enumerate(prices):
                timestamp = price_point[0] / 1000  # Convert to seconds
                price = price_point[1]
                
                # Calculer le sentiment basé sur la tendance du prix
                sentiment_score = 0
                if i > 0:
                    prev_price = prices[i-1][1]
                    price_change = (price - prev_price) / prev_price * 100
                    
                    if price_change > 0.5:
                        sentiment_score = min(0.8, 0.2 + (price_change / 10))
                    elif price_change < -0.5:
                        sentiment_score = max(-0.8, -0.2 + (price_change / 10))
                    else:
                        sentiment_score = price_change / 20  # Neutre avec légère variation
                
                historical_data.append({
                    'time': datetime.fromtimestamp(timestamp).strftime('%H:%M'),
                    'price': round(price, 2),
                    'sentiment': round(sentiment_score, 3)
                })
            
            # Mettre en cache
            history_cache = {'timestamp': now, 'data': historical_data}
            return historical_data
            
    except Exception as e:
        print(f"Erreur API CoinGecko History: {e}")
    
    # Fallback sur données simulées
    return generate_historical_data(24)

# --- DONNÉES SIMULÉES AMÉLIORÉES ---
CRYPTO_POSTS = {
    'positive': [
        "Bitcoin just hit a new support level, looking bullish! 🚀",
        "Just bought the dip! Diamond hands 💎🙌",
        "Ethereum ETF approved! This is HUGE for the market!",
        "Institutional adoption is increasing every day.",
        "HODL till 100k! The moon is close 🌙",
        "Best time to accumulate BTC. Thank me later.",
        "Crypto is the future of finance. Period.",
        "Mass adoption incoming! Banks are scared.",
        "DeFi is revolutionizing everything! 🔥",
        "Bitcoin dominance rising, altseason coming!"
    ],
    'negative': [
        "Why is the market crashing today? I'm scared 😰",
        "Regulation news is bad for crypto...",
        "Is it too late to buy BTC? Already missed the boat.",
        "Lost all my money on meme coins, crypto is a scam.",
        "Sell everything before it drops to zero!",
        "Another exchange hack. When will this stop?",
        "Whales manipulating the market again 🐋",
        "Government crackdown incoming. Be careful.",
        "BTC is dead, long live gold.",
        "Rugpull season. Trust no one."
    ],
    'neutral': [
        "What's the best wallet for beginners?",
        "Can someone explain staking to me?",
        "BTC vs ETH, which one to buy?",
        "When is the next halving event?",
        "How to calculate crypto taxes?",
        "What's your portfolio allocation?",
        "Best exchange for low fees?",
        "Hardware wallet recommendations?"
    ]
}

# --- FONCTION 1 : PRIX CRYPTO AVEC CACHE ---
def get_crypto_data(crypto_id='bitcoin'):
    """Récupère les données crypto avec système de cache"""
    global price_cache
    
    # Vérifier le cache
    now = datetime.now()
    if price_cache['timestamp'] and (now - price_cache['timestamp']).seconds < CACHE_DURATION:
        return price_cache['data']
    
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    params = {
        'localization': 'false',
        'tickers': 'false',
        'community_data': 'false',
        'developer_data': 'false'
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        result = {
            'name': data['name'],
            'symbol': data['symbol'].upper(),
            'price': data['market_data']['current_price']['usd'],
            'change_24h': round(data['market_data']['price_change_percentage_24h'], 2),
            'market_cap': data['market_data']['market_cap']['usd'],
            'volume_24h': data['market_data']['total_volume']['usd'],
            'high_24h': data['market_data']['high_24h']['usd'],
            'low_24h': data['market_data']['low_24h']['usd'],
            'image': data['image']['small']
        }
        
        # Mettre en cache
        price_cache = {'timestamp': now, 'data': result}
        return result
        
    except Exception as e:
        print(f"Erreur API CoinGecko: {e}")
        return {
            'name': 'Bitcoin',
            'symbol': 'BTC',
            'price': 0,
            'change_24h': 0,
            'market_cap': 0,
            'volume_24h': 0,
            'high_24h': 0,
            'low_24h': 0,
            'image': None,
            'error': True
        }

# --- FONCTION 2 : ANALYSE DE SENTIMENT AMÉLIORÉE ---
def get_sentiment_analysis(num_posts=10):
    """Analyse de sentiment avec statistiques détaillées"""
    
    # Sélectionner des posts aléatoires (mélange des sentiments)
    all_posts = []
    all_posts.extend(random.sample(CRYPTO_POSTS['positive'], min(4, len(CRYPTO_POSTS['positive']))))
    all_posts.extend(random.sample(CRYPTO_POSTS['negative'], min(3, len(CRYPTO_POSTS['negative']))))
    all_posts.extend(random.sample(CRYPTO_POSTS['neutral'], min(3, len(CRYPTO_POSTS['neutral']))))
    random.shuffle(all_posts)
    
    selected_posts = all_posts[:num_posts]
    
    # Analyser chaque post
    scores = []
    analyzed_posts = []
    
    for post in selected_posts:
        sentiment = analyzer.polarity_scores(post)
        compound_score = sentiment['compound']
        scores.append(compound_score)
        
        # Classifier le post
        if compound_score >= 0.05:
            classification = 'Positif'
            emoji = '<i class="fas fa-smile text-emerald-400"></i>'
            color = 'emerald'
        elif compound_score <= -0.05:
            classification = 'Négatif'
            emoji = '<i class="fas fa-frown text-red-400"></i>'
            color = 'red'
        else:
            classification = 'Neutre'
            emoji = '<i class="fas fa-meh text-gray-400"></i>'
            color = 'gray'
        
        analyzed_posts.append({
            'text': post,
            'score': round(compound_score, 3),
            'classification': classification,
            'emoji': emoji,
            'color': color
        })
    
    # Calculer les statistiques
    average_score = sum(scores) / len(scores)
    positive_count = sum(1 for s in scores if s >= 0.05)
    negative_count = sum(1 for s in scores if s <= -0.05)
    neutral_count = len(scores) - positive_count - negative_count
    
    # Déterminer le sentiment global
    if average_score >= 0.05:
        overall = {'label': 'Positif', 'color': 'emerald', 'emoji': '<i class="fas fa-rocket text-emerald-400 text-4xl"></i>'}
    elif average_score <= -0.05:
        overall = {'label': 'Négatif', 'color': 'red', 'emoji': '<i class="fas fa-exclamation-triangle text-red-400 text-4xl"></i>'}
    else:
        overall = {'label': 'Neutre', 'color': 'gray', 'emoji': '<i class="fas fa-balance-scale text-gray-400 text-4xl"></i>'}
    
    return {
        'overall': overall,
        'score': round(average_score, 3),
        'posts': analyzed_posts,
        'stats': {
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'total': len(scores)
        }
    }

# --- FONCTION 3 : GÉNÉRER DONNÉES HISTORIQUES ---
def generate_historical_data(hours=24):
    """Génère des données historiques pour le graphique"""
    data = []
    base_price = 43000
    base_sentiment = 0.2
    
    for i in range(hours):
        # Simuler une volatilité réaliste
        price_change = random.uniform(-0.02, 0.02)
        sentiment_change = random.uniform(-0.1, 0.1)
        
        base_price *= (1 + price_change)
        base_sentiment = max(-1, min(1, base_sentiment + sentiment_change))
        
        timestamp = (datetime.now() - timedelta(hours=hours-i)).strftime('%H:%M')
        
        data.append({
            'time': timestamp,
            'price': round(base_price, 2),
            'sentiment': round(base_sentiment, 3)
        })
    
    return data

# --- FONCTION 4 : STEADY NEWS API ---
def get_steady_news():
    """Simule l'API Steady pour les actualités financières"""
    # Récupérer la clé API depuis l'environnement
    steady_api_key = os.getenv('STEADY_API_KEY')
    
    # Articles fictifs réalistes
    news_articles = [
        {
            'title': 'Bitcoin ETF approval drives institutional adoption surge',
            'source': 'Bloomberg',
            'published_at': datetime.now() - timedelta(hours=2)
        },
        {
            'title': 'Major cryptocurrency exchange faces regulatory scrutiny',
            'source': 'CoinDesk',
            'published_at': datetime.now() - timedelta(hours=4)
        },
        {
            'title': 'Federal Reserve hints at digital dollar development',
            'source': 'Reuters',
            'published_at': datetime.now() - timedelta(hours=6)
        },
        {
            'title': 'Crypto market volatility reaches new monthly high',
            'source': 'Financial Times',
            'published_at': datetime.now() - timedelta(hours=8)
        },
        {
            'title': 'Blockchain technology adoption accelerates in banking sector',
            'source': 'Wall Street Journal',
            'published_at': datetime.now() - timedelta(hours=12)
        }
    ]
    
    # Analyser le sentiment de chaque article
    analyzed_articles = []
    scores = []
    
    for article in news_articles:
        sentiment = analyzer.polarity_scores(article['title'])
        compound_score = sentiment['compound']
        scores.append(compound_score)
        
        # Classifier l'article
        if compound_score >= 0.05:
            classification = 'Positif'
            badge_color = 'emerald'
            icon = '<i class="fas fa-arrow-up text-emerald-500"></i>'
        elif compound_score <= -0.05:
            classification = 'Négatif'
            badge_color = 'red'
            icon = '<i class="fas fa-arrow-down text-red-500"></i>'
        else:
            classification = 'Neutre'
            badge_color = 'amber'
            icon = '<i class="fas fa-minus text-amber-500"></i>'
        
        analyzed_articles.append({
            'title': article['title'],
            'source': article['source'],
            'published_at': article['published_at'].strftime('%H:%M'),
            'sentiment_score': round(compound_score, 3),
            'classification': classification,
            'badge_color': badge_color,
            'icon': icon
        })
    
    # Calculer le sentiment global
    average_score = sum(scores) / len(scores)
    positive_count = sum(1 for s in scores if s >= 0.05)
    negative_count = sum(1 for s in scores if s <= -0.05)
    neutral_count = len(scores) - positive_count - negative_count
    
    # Déterminer le sentiment global
    if average_score >= 0.05:
        overall_sentiment = {
            'label': 'Positif',
            'color': 'emerald',
            'icon': '<i class="fas fa-chart-line text-emerald-500 text-4xl"></i>',
            'description': 'Les actualités sont globalement positives'
        }
    elif average_score <= -0.05:
        overall_sentiment = {
            'label': 'Négatif',
            'color': 'red',
            'icon': '<i class="fas fa-chart-line-down text-red-500 text-4xl"></i>',
            'description': 'Les actualités montrent des préoccupations'
        }
    else:
        overall_sentiment = {
            'label': 'Neutre',
            'color': 'amber',
            'icon': '<i class="fas fa-balance-scale text-amber-500 text-4xl"></i>',
            'description': 'Sentiment équilibré dans les actualités'
        }
    
    return {
        'articles': analyzed_articles,
        'overall_sentiment': overall_sentiment,
        'average_score': round(average_score, 3),
        'stats': {
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'total': len(scores)
        },
        'api_key_used': steady_api_key is not None
    }

# --- FONCTION 5 : TWITTER API ---
def get_twitter_data():
    """Récupère les tweets Bitcoin avec fallback sur mock data"""
    twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    # Mock tweets réalistes pour fallback
    mock_tweets = [
        "Bitcoin just broke $45k resistance! Next stop moon 🚀 #BTC #crypto",
        "Massive institutional adoption happening right now. This is just the beginning.",
        "Market looking bearish today. Time to DCA and HODL 💎🙌",
        "Why is everyone panicking? This is just a healthy correction.",
        "Bitcoin ETF approval could be the catalyst we've been waiting for",
        "Regulation FUD again... when will people learn? #Bitcoin",
        "Just bought more BTC. Thank me later 📈",
        "Crypto winter is over. Bull run incoming! 🐂",
        "Another day, another Bitcoin all-time high incoming",
        "Whales are accumulating. Smart money knows what's up."
    ]
    
    tweets_data = []
    api_success = False
    
    # Tentative d'appel à l'API Twitter
    if twitter_bearer_token:
        try:
            headers = {
                'Authorization': f'Bearer {twitter_bearer_token}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'query': 'bitcoin OR BTC OR cryptocurrency',
                'max_results': 10,
                'tweet.fields': 'created_at,author_id,public_metrics'
            }
            
            response = requests.get(
                'https://api.twitter.com/2/tweets/search/recent',
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    for tweet in data['data'][:10]:
                        tweets_data.append({
                            'text': tweet['text'],
                            'created_at': tweet.get('created_at', ''),
                            'author_id': tweet.get('author_id', 'unknown'),
                            'is_mock': False
                        })
                    api_success = True
            else:
                print(f"Twitter API Error: {response.status_code}")
                
        except Exception as e:
            print(f"Twitter API Exception: {e}")
    
    # Fallback sur mock data si API échoue
    if not api_success or not tweets_data:
        for i, tweet_text in enumerate(mock_tweets):
            tweets_data.append({
                'text': tweet_text,
                'created_at': (datetime.now() - timedelta(minutes=i*15)).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                'author_id': f'user_{i+1}',
                'is_mock': True
            })
    
    # Analyser le sentiment de chaque tweet
    analyzed_tweets = []
    scores = []
    
    for tweet in tweets_data:
        sentiment = analyzer.polarity_scores(tweet['text'])
        compound_score = sentiment['compound']
        scores.append(compound_score)
        
        # Classifier le tweet
        if compound_score >= 0.05:
            classification = 'Positif'
            color = 'emerald'
            icon = '<i class="fas fa-arrow-up text-emerald-400"></i>'
        elif compound_score <= -0.05:
            classification = 'Négatif'
            color = 'red'
            icon = '<i class="fas fa-arrow-down text-red-400"></i>'
        else:
            classification = 'Neutre'
            color = 'sky'
            icon = '<i class="fas fa-minus text-sky-400"></i>'
        
        # Formater la date
        try:
            if tweet['created_at']:
                created_time = datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00'))
                time_ago = created_time.strftime('%H:%M')
            else:
                time_ago = 'Maintenant'
        except:
            time_ago = 'Maintenant'
        
        analyzed_tweets.append({
            'text': tweet['text'],
            'time_ago': time_ago,
            'author_id': tweet['author_id'],
            'sentiment_score': round(compound_score, 3),
            'classification': classification,
            'color': color,
            'icon': icon,
            'is_mock': tweet['is_mock']
        })
    
    # Calculer les statistiques
    average_score = sum(scores) / len(scores) if scores else 0
    positive_count = sum(1 for s in scores if s >= 0.05)
    negative_count = sum(1 for s in scores if s <= -0.05)
    neutral_count = len(scores) - positive_count - negative_count
    
    # Calculer le Hype Meter (0-100)
    hype_meter = max(0, min(100, int((average_score + 1) * 50)))
    
    # Déterminer le niveau de hype
    if hype_meter >= 70:
        hype_level = {'label': 'TRÈS HYPE', 'color': 'emerald', 'emoji': '🚀'}
    elif hype_meter >= 50:
        hype_level = {'label': 'HYPE', 'color': 'sky', 'emoji': '📈'}
    elif hype_meter >= 30:
        hype_level = {'label': 'NEUTRE', 'color': 'amber', 'emoji': '😐'}
    else:
        hype_level = {'label': 'BEARISH', 'color': 'red', 'emoji': '📉'}
    
    return {
        'tweets': analyzed_tweets,
        'hype_meter': hype_meter,
        'hype_level': hype_level,
        'average_score': round(average_score, 3),
        'stats': {
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'total': len(scores)
        },
        'api_success': api_success,
        'is_simulation': not api_success
    }

# --- FONCTION 6 : TELEGRAM SIGNALS ---
def get_telegram_signals():
    """Simule la réception de signaux Telegram de trading"""
    
    # Canaux fictifs
    channels = [
        {'name': 'Crypto Whales 🐋', 'members': '45.2K', 'status': 'active'},
        {'name': 'Pump Signals 🚀', 'members': '23.8K', 'status': 'active'},
        {'name': 'DeFi Alerts 🌐', 'members': '18.5K', 'status': 'active'},
        {'name': 'Whale Movements', 'members': '67.1K', 'status': 'active'},
        {'name': 'Technical Analysis', 'members': '31.4K', 'status': 'active'}
    ]
    
    # Messages de signaux réalistes
    signal_messages = [
        {
            'text': '🟢 BUY SIGNAL: Bitcoin (BTC) - Strong bullish momentum detected! Entry: $44,500',
            'channel': 'Crypto Whales 🐋',
            'signal_type': 'ACHAT',
            'crypto': 'BTC',
            'entry_price': 44500,
            'time_ago': '2 min'
        },
        {
            'text': '🔴 SELL ALERT: Ethereum showing weakness. Consider taking profits at $2,650',
            'channel': 'Technical Analysis',
            'signal_type': 'VENTE',
            'crypto': 'ETH',
            'entry_price': 2650,
            'time_ago': '5 min'
        },
        {
            'text': '🐋 WHALE ALERT: 1,000 BTC moved to exchange. Possible dump incoming!',
            'channel': 'Whale Movements',
            'signal_type': 'ALERTE',
            'crypto': 'BTC',
            'entry_price': 44200,
            'time_ago': '8 min'
        },
        {
            'text': '🚀 PUMP DETECTED: Solana (SOL) breaking resistance! Quick scalp opportunity',
            'channel': 'Pump Signals 🚀',
            'signal_type': 'ACHAT',
            'crypto': 'SOL',
            'entry_price': 98.50,
            'time_ago': '12 min'
        },
        {
            'text': '🌐 DeFi UPDATE: Uniswap (UNI) governance proposal passed. Bullish for UNI',
            'channel': 'DeFi Alerts 🌐',
            'signal_type': 'INFO',
            'crypto': 'UNI',
            'entry_price': 7.25,
            'time_ago': '15 min'
        },
        {
            'text': '⚠️ RISK WARNING: High volatility expected in next 2 hours. Manage positions carefully',
            'channel': 'Technical Analysis',
            'signal_type': 'ALERTE',
            'crypto': 'MARKET',
            'entry_price': 0,
            'time_ago': '18 min'
        },
        {
            'text': '💰 ARBITRAGE OPPORTUNITY: Price difference detected between exchanges for ADA',
            'channel': 'Crypto Whales 🐋',
            'signal_type': 'ACHAT',
            'crypto': 'ADA',
            'entry_price': 0.52,
            'time_ago': '22 min'
        }
    ]
    
    # Analyser chaque signal
    analyzed_signals = []
    scores = []
    
    for signal in signal_messages:
        sentiment = analyzer.polarity_scores(signal['text'])
        compound_score = sentiment['compound']
        scores.append(compound_score)
        
        # Calculer le score de confiance (0-100)
        confidence_score = max(10, min(95, int((abs(compound_score) + 0.2) * 80)))
        
        # Déterminer la couleur selon le type de signal
        if signal['signal_type'] == 'ACHAT':
            color = 'emerald'
            icon = '<i class="fas fa-arrow-up text-emerald-400"></i>'
            bg_color = 'emerald-900/20'
        elif signal['signal_type'] == 'VENTE':
            color = 'red'
            icon = '<i class="fas fa-arrow-down text-red-400"></i>'
            bg_color = 'red-900/20'
        elif signal['signal_type'] == 'ALERTE':
            color = 'amber'
            icon = '<i class="fas fa-exclamation-triangle text-amber-400"></i>'
            bg_color = 'amber-900/20'
        else:  # INFO
            color = 'cyan'
            icon = '<i class="fas fa-info-circle text-cyan-400"></i>'
            bg_color = 'cyan-900/20'
        
        analyzed_signals.append({
            'text': signal['text'],
            'channel': signal['channel'],
            'signal_type': signal['signal_type'],
            'crypto': signal['crypto'],
            'entry_price': signal['entry_price'],
            'time_ago': signal['time_ago'],
            'confidence_score': confidence_score,
            'sentiment_score': round(compound_score, 3),
            'color': color,
            'icon': icon,
            'bg_color': bg_color
        })
    
    # Calculer les statistiques
    buy_signals = sum(1 for s in analyzed_signals if s['signal_type'] == 'ACHAT')
    sell_signals = sum(1 for s in analyzed_signals if s['signal_type'] == 'VENTE')
    alert_signals = sum(1 for s in analyzed_signals if s['signal_type'] in ['ALERTE', 'INFO'])
    
    # Score de confiance global
    avg_confidence = sum(s['confidence_score'] for s in analyzed_signals) / len(analyzed_signals)
    
    # Déterminer le sentiment global du marché
    if buy_signals > sell_signals:
        market_sentiment = {
            'label': 'BULLISH',
            'color': 'emerald',
            'description': 'Plus de signaux d\'achat détectés'
        }
    elif sell_signals > buy_signals:
        market_sentiment = {
            'label': 'BEARISH',
            'color': 'red',
            'description': 'Plus de signaux de vente détectés'
        }
    else:
        market_sentiment = {
            'label': 'NEUTRE',
            'color': 'cyan',
            'description': 'Marché équilibré'
        }
    
    return {
        'channels': channels,
        'signals': analyzed_signals,
        'market_sentiment': market_sentiment,
        'avg_confidence': round(avg_confidence, 1),
        'stats': {
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'alert_signals': alert_signals,
            'total': len(analyzed_signals)
        },
        'telegram_config': {
            'api_id': os.getenv('TELEGRAM_API_ID'),
            'phone': os.getenv('TELEGRAM_PHONE'),
            'is_configured': bool(os.getenv('TELEGRAM_API_ID') and os.getenv('TELEGRAM_PHONE'))
        }
    }

# --- ROUTES ---

@app.route('/')
def index():
    """Page principale"""
    crypto_data = get_crypto_data('bitcoin')
    sentiment_data = get_sentiment_analysis(10)
    historical_data = get_real_history('bitcoin')
    
    return render_template('index.html', 
                         crypto=crypto_data, 
                         sentiment=sentiment_data,
                         history=historical_data)

@app.route('/api/refresh-sentiment')
def refresh_sentiment():
    """API pour rafraîchir uniquement le sentiment"""
    sentiment_data = get_sentiment_analysis(10)
    return jsonify(sentiment_data)

@app.route('/api/refresh-price')
def refresh_price():
    """API pour rafraîchir uniquement le prix"""
    crypto_data = get_crypto_data('bitcoin')
    return jsonify(crypto_data)

@app.route('/api/crypto/<crypto_id>')
def get_crypto(crypto_id):
    """API pour obtenir les données d'une crypto spécifique"""
    crypto_data = get_crypto_data(crypto_id)
    return jsonify(crypto_data)

@app.route('/api/history/<coin_id>')
def get_history_api(coin_id):
    """API pour obtenir l'historique d'une crypto spécifique"""
    historical_data = get_real_history(coin_id)
    
    # Déterminer le label de la crypto
    crypto_labels = {
        'bitcoin': 'Bitcoin',
        'ethereum': 'Ethereum', 
        'solana': 'Solana'
    }
    
    return jsonify({
        'label': crypto_labels.get(coin_id, coin_id.capitalize()),
        'data': historical_data
    })

@app.route('/dashboard/steady')
def steady_dashboard():
    """Dashboard Steady API - Analyse de sentiment des actualités"""
    news_data = get_steady_news()
    return render_template('dash_steady.html', news=news_data)

@app.route('/dashboard/twitter')
def twitter_dashboard():
    """Dashboard Twitter/X - Analyse de sentiment des tweets"""
    twitter_data = get_twitter_data()
    return render_template('dash_twitter.html', twitter=twitter_data)

@app.route('/dashboard/telegram')
def telegram_dashboard():
    """Dashboard Telegram - Signaux de trading"""
    telegram_data = get_telegram_signals()
    return render_template('dash_telegram.html', telegram=telegram_data)

if __name__ == '__main__':
    print("CryptoSaaS Server Starting...")
    print("Dashboard: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)