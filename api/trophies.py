 PY
Copier

from http.server import BaseHTTPRequestHandler
import json
from psnawp_api import PSNAWP
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Récupère le token NPSSO depuis les variables d'environnement
            npsso_token = os.environ.get('ytRANQi9XCazRZ6NsTFYDP39wUAOsNIOnN2Dcp7yKPpb5iXCVXfdu8bzwVzGzyKT')
            
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
            online_id = client.online_id
            account_id = client.account_id
            
            # Récupère le résumé des trophées
            trophy_summary = client.trophy_summary()
            
            # Prépare la réponse JSON
            response_data = {
                'online_id': online_id,
                'account_id': account_id,
                'level': trophy_summary.trophy_level,
                'progress': trophy_summary.progress,
                'trophies': {
                    'platinum': trophy_summary.earned_trophies.platinum,
                    'gold': trophy_summary.earned_trophies.gold,
                    'silver': trophy_summary.earned_trophies.silver,
                    'bronze': trophy_summary.earned_trophies.bronze
                },
                'total_trophies': (
                    trophy_summary.earned_trophies.platinum + 
                    trophy_summary.earned_trophies.gold + 
                    trophy_summary.earned_trophies.silver + 
                    trophy_summary.earned_trophies.bronze
                )
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
