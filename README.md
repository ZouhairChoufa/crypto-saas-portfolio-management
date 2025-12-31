# CryptoSaaS - Enterprise Sentiment Analysis Platform

## Description

Plateforme SaaS professionnelle d'analyse de sentiment crypto avec 4 dashboards intégrés :
- **Market Dashboard** - Prix crypto en temps réel (CoinGecko API)
- **News Sentiment** - Analyse d'actualités financières (Steady API)
- **Social Media** - Sentiment Twitter/X avec Hype Meter
- **Trading Signals** - Signaux Telegram avec scores de confiance

**Développé par :** CHOUFA Zouhair & Oulhadj Belaid  
**Encadrant :** Mr. BENI-HSSANE  
**Année :** 2024-2025

---

## Technologies Utilisées

### Backend
- **Python 3.12+**
- **Flask 3.0** - Framework Web moderne
- **VADER Sentiment** - Analyse NLP avancée
- **CoinGecko API** - Données crypto temps réel
- **Twitter API v2** - Données sociales
- **Telegram MTProto** - Signaux de trading

### Frontend
- **HTML5 / CSS3** avec Dark/Light Mode
- **Tailwind CSS** - Framework UI Enterprise
- **Font Awesome 6.5** - Icônes professionnelles
- **Chart.js** - Visualisations interactives dynamiques
- **Inter Font** - Typographie moderne

### Architecture
- **Modular Design** - Structure MVC propre
- **Environment Variables** - Configuration sécurisée
- **Error Handling** - Gestion d'erreurs robuste
- **Responsive Design** - Compatible mobile/desktop

---

## Installation

### 1. Cloner le Projet
```bash
git clone https://github.com/votre-username/crypto-saas.git
cd crypto-saas
```

### 2. Créer un Environnement Virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les Dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration Environnement
Copier `.env.example` vers `.env` et configurer :
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# API Keys
COINGECKO_API_KEY=your-coingecko-key
STEADY_API_KEY=your-steady-key
TWITTER_BEARER_TOKEN=your-twitter-token

# Telegram Config
TELEGRAM_API_ID=your-api-id
TELEGRAM_API_HASH=your-api-hash
TELEGRAM_PHONE=your-phone-number
```

### 5. Lancer le Serveur
```bash
python app.py
```

### 6. Accéder aux Dashboards
- **Market:** http://127.0.0.1:5000/
- **News:** http://127.0.0.1:5000/dashboard/steady
- **Social:** http://127.0.0.1:5000/dashboard/twitter
- **Signals:** http://127.0.0.1:5000/dashboard/telegram

---

## Fonctionnalités

### Dashboards Implémentés
- [x] **Market Dashboard** - Prix Bitcoin/Ethereum/Solana en temps réel
- [x] **News Sentiment** - Analyse d'actualités avec scores VADER
- [x] **Social Media** - Hype Meter Twitter avec feed authentique
- [x] **Trading Signals** - Signaux Telegram avec scores de confiance
- [x] **Navigation Unifiée** - Barre de navigation moderne
- [x] **Design Responsive** - Compatible tous écrans
- [x] **Dark/Light Mode** - Interface adaptative professionnelle

### Fonctionnalités Techniques
- [x] **Système de Cache** - Optimisation requêtes API (10s)
- [x] **Fallback System** - Mode simulation si APIs indisponibles
- [x] **Error Handling** - Gestion gracieuse des erreurs
- [x] **Environment Config** - Variables d'environnement sécurisées
- [x] **Modular Architecture** - Code organisé et maintenable
- [x] **Unit Tests** - Tests automatisés (pytest)
- [x] **Real-time Data** - Données crypto en temps réel (CoinGecko)
- [x] **Smart Sentiment** - Calcul intelligent basé sur tendances prix

### Améliorations Futures
- [ ] Base de données PostgreSQL
- [ ] Authentification utilisateur
- [ ] Alertes push/email
- [ ] API REST complète
- [ ] Dashboard personnalisable
- [ ] Historique des données

---

## Structure du Projet

```
crypto-saas/
├── app.py                    # Application Flask principale
├── requirements.txt          # Dépendances Python
├── .env                     # Variables d'environnement
├── .gitignore              # Fichiers à ignorer
├── README.md               # Documentation
│
├── templates/              # Templates HTML
│   ├── base.html          # Template de base
│   ├── index.html         # Dashboard Market
│   ├── dash_steady.html   # Dashboard News
│   ├── dash_twitter.html  # Dashboard Social
│   └── dash_telegram.html # Dashboard Signals
│
├── static/                # Fichiers statiques
│   ├── css/style.css     # Styles personnalisés
│   ├── js/main.js        # JavaScript
│   └── images/           # Images et logos
│
├── utils/                 # Modules utilitaires
│   ├── __init__.py
│   ├── crypto_api.py     # API CoinGecko
│   └── sentiment.py     # Analyse sentiment
│
├── models/               # Modèles de données
│   └── __init__.py
│
└── tests/               # Tests unitaires
    ├── __init__.py
    ├── test_api.py
    └── test_sentiment.py
```

---

## API Endpoints

### Dashboards
- `GET /` - Market Dashboard (CoinGecko)
- `GET /dashboard/steady` - News Sentiment
- `GET /dashboard/twitter` - Social Media Analysis
- `GET /dashboard/telegram` - Trading Signals

### API Routes
- `GET /api/refresh-sentiment` - Rafraîchir sentiment
- `GET /api/refresh-price` - Rafraîchir prix
- `GET /api/crypto/<crypto_id>` - Données crypto spécifique
- `GET /api/history/<coin_id>` - Historique prix + sentiment (24h)

---

## Tests

```bash
# Installer pytest
pip install pytest

# Lancer tous les tests
pytest tests/ -v

# Tests avec couverture
pip install pytest-cov
pytest tests/ --cov=utils --cov-report=html
```

---

## Fonctionnalités Avancées

### Graphique Dynamique
- **Sélecteur Multi-Crypto** - Bitcoin, Ethereum, Solana
- **Double Axe Y** - Prix ($) et Sentiment (-1 à +1)
- **Tooltips Interactifs** - Informations détaillées au survol
- **Données Temps Réel** - API CoinGecko avec cache intelligent
- **Sentiment Calculé** - Basé sur les tendances de prix

### Interface Enterprise
- **Dark/Light Mode** - Basculement automatique avec localStorage
- **Design Responsive** - Compatible mobile/desktop
- **Navigation Moderne** - Sidebar sticky avec icônes FontAwesome
- **Animations Fluides** - Transitions CSS et Chart.js
- **Zéro Émoji** - Interface professionnelle

## Intelligence Artificielle

### VADER Sentiment Analysis
- **Spécialisé réseaux sociaux** - Comprend emojis et argot crypto
- **Score de -1 à +1** - Négatif → Neutre → Positif
- **Analyse contextuelle** - Détecte sarcasme et amplificateurs
- **Temps réel** - Traitement instantané des messages

### Exemples d'Analyse
```python
"Bitcoin to the moon!" → Score: +0.62 (Très Positif)
"Market crash incoming" → Score: -0.54 (Négatif)
"HODL diamond hands" → Score: +0.45 (Positif)
"What's the best wallet?" → Score: 0.03 (Neutre)
```

---

## Déploiement GitHub

### 1. Préparer le Repository
```bash
# Initialiser Git
git init
git add .
git commit -m "Initial commit: CryptoSaaS v1.0"

# Ajouter remote GitHub
git remote add origin https://github.com/votre-username/crypto-saas-portfolio-management.git
git branch -M main
git push -u origin main
```

### 2. Configuration GitHub
- Créer un repository public/privé
- Ajouter une description : "Multi-platform crypto sentiment analysis SaaS"
- Tags : `python`, `flask`, `cryptocurrency`, `sentiment-analysis`, `tailwindcss`

### 3. GitHub Actions (Optionnel)
Créer `.github/workflows/tests.yml` pour CI/CD automatique

### 4. Documentation
- README.md complet 
- Screenshots dans `/docs/screenshots/`
- Documentation API avec Swagger (futur)

---

## Sécurité

### Variables Sensibles
- **Ne jamais commiter** les clés API dans `.env`
- **Utiliser** `.env.example` comme template
- **Ajouter** `.env` dans `.gitignore`

### Bonnes Pratiques
- Rotation régulière des clés API
- Validation des entrées utilisateur
- Rate limiting sur les endpoints
- HTTPS en production

---

## Métriques du Projet

- **Lignes de Code :** ~2000+ lignes
- **Templates HTML :** 5 fichiers
- **Modules Python :** 8 modules
- **APIs Intégrées :** 4 sources de données
- **Tests Unitaires :** 15+ tests
- **Couverture Code :** 85%+

---

## Dépannage

### Problèmes Courants

**Erreur ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**API Rate Limiting**
- CoinGecko : 10-30 req/min (gratuit)
- Twitter : 300 req/15min
- Solution : Cache système intégré

**Encoding Windows**
- Utiliser UTF-8 dans l'éditeur
- Variables d'environnement sans emojis

---

## Licence

**Projet Académique** - Tous droits réservés  
© 2025 CHOUFA Zouhair & Oulhadj Belaid

Ce projet est développé dans le cadre d'un projet de fin d'études.  
Utilisation commerciale interdite sans autorisation.

---

## Contribution

### Développeurs Principaux
- **CHOUFA Zouhair** - Lead Developer & UI/UX
- **Oulhadj Belaid** - Backend Developer & API Integration

### Encadrement Académique
- **Mr. BENI-HSSANE** - Superviseur de projet

### Contact
- Email : [zouhair.choufa3@gmail.com]
- GitHub : [[github.com/ZouhairChoufa/crypto-saas-portfolio-management](https://github.com/ZouhairChoufa/crypto-saas-portfolio-management)]
- Demo : [cryptosaas-portfolio-management-demo.herokuapp.com]

---

## Remerciements

### APIs & Services
- **CoinGecko** - Données crypto gratuites et fiables
- **Twitter API** - Accès aux données sociales
- **Steady API** - Actualités financières
- **Telegram** - Plateforme de signaux

### Technologies
- **Flask Team** - Framework web Python
- **VADER Team** - Modèle NLP open-source
- **Tailwind CSS** - Framework UI moderne
- **Chart.js** - Bibliothèque de graphiques
- **Font Awesome** - Icônes professionnelles

### Communauté
- **Stack Overflow** - Résolution de problèmes
- **GitHub Community** - Inspiration et exemples
- **Python Community** - Documentation et support

---

**Développé pour l'analyse de sentiment crypto**  
*Projet de fin De module SA & TM 2024-2025*