from http.server import BaseHTTPRequestHandler
import json
from psnawp_api import PSNAWP
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Récupère le token NPSSO depuis les variables d'environnement
            npsso_token = os.environ.get('NPSSO_TOKEN')
            
            if not npsso_token:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'NPSSO_TOKEN non configuré'
                }).encode())
                return
            
            # Connexion à PSN
            psnawp = PSNAWP(npsso_token)
            client = psnawp.me()
            
            # Récupère les informations du profil
            profile = client.profile()
            trophy_summary = client.trophy_summary()
            
            # Récupère les jeux récents
            title_stats = client.title_stats(limit=5)
            recent_games = []
            
            for game in title_stats:
                recent_games.append({
                    'name': game.get('name', 'Jeu inconnu'),
                    'play_duration': game.get('play_duration', 'N/A')
                })
            
            # Prépare la réponse JSON
            response_data = {
                'online_id': profile.get('onlineId', 'N/A'),
                'level': trophy_summary.get('accountLevel', 0),
                'trophies': {
                    'platinum': trophy_summary.get('earnedTrophies', {}).get('platinum', 0),
                    'gold': trophy_summary.get('earnedTrophies', {}).get('gold', 0),
                    'silver': trophy_summary.get('earnedTrophies', {}).get('silver', 0),
                    'bronze': trophy_summary.get('earnedTrophies', {}).get('bronze', 0)
                },
                'total_trophies': trophy_summary.get('earnedTrophies', {}).get('bronze', 0) + 
                                 trophy_summary.get('earnedTrophies', {}).get('silver', 0) + 
                                 trophy_summary.get('earnedTrophies', {}).get('gold', 0) + 
                                 trophy_summary.get('earnedTrophies', {}).get('platinum', 0),
                'recent_games': recent_games[:3]  # Top 3 jeux récents
            }
            
            # Envoie la réponse
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e)
            }).encode())
