# Widget PSN pour Widgy

Ce projet te permet de récupérer tes trophées PlayStation pour les afficher dans un widget Widgy sur iOS.

## 📋 Prérequis

1. Un compte GitHub (gratuit)
2. Un compte Vercel (gratuit)
3. Ton token NPSSO PlayStation

## 🔑 Récupérer ton token NPSSO

1. Va sur https://ca.account.sony.com/api/v1/ssocookie
2. Connecte-toi avec ton compte PlayStation
3. Tu verras une page avec du texte comme `{"npsso":"xxxxxxxx"}`
4. Copie la valeur entre guillemets (le code long après "npsso":")
5. **Important** : Ce token expire après ~2 mois, il faudra le renouveler

## 🚀 Installation sur Vercel

### Méthode 1 : Déploiement direct

1. Va sur https://vercel.com
2. Connecte-toi avec GitHub
3. Clique sur "Add New" → "Project"
4. Importe ce dossier depuis GitHub
5. Dans "Environment Variables", ajoute :
   - Name: `NPSSO_TOKEN`
   - Value: ton token NPSSO copié plus haut
6. Clique sur "Deploy"
7. Attend que le déploiement se termine (2-3 minutes)
8. Note l'URL de ton projet (ex: `https://ton-projet.vercel.app`)

### Méthode 2 : CLI Vercel (si tu es à l'aise avec le terminal)

```bash
# Installe Vercel CLI
npm i -g vercel

# Dans le dossier du projet
vercel

# Suis les instructions
# Quand demandé, ajoute la variable d'environnement NPSSO_TOKEN
```

## 📱 Configuration dans Widgy

1. Ouvre Widgy sur ton iPhone
2. Crée un nouveau widget
3. Ajoute un élément "JSON"
4. Configure l'URL : `https://ton-projet.vercel.app/api/trophies`
5. Définis l'intervalle de rafraîchissement (ex: 30 minutes)

### Données disponibles

Le JSON retourné contient :

```json
{
  "online_id": "TonPseudo",
  "level": 342,
  "trophies": {
    "platinum": 12,
    "gold": 145,
    "silver": 432,
    "bronze": 1250
  },
  "total_trophies": 1839,
  "recent_games": [
    {
      "name": "Spider-Man 2",
      "play_duration": "45h 32m"
    }
  ]
}
```

### Exemple de mapping Widgy

- Niveau : `${level}`
- Platines : `${trophies.platinum}`
- Or : `${trophies.gold}`
- Argent : `${trophies.silver}`
- Bronze : `${trophies.bronze}`
- Total : `${total_trophies}`
- Jeu récent : `${recent_games[0].name}`

## 🔧 Dépannage

### Erreur "NPSSO_TOKEN non configuré"
→ Vérifie que tu as bien ajouté la variable d'environnement dans Vercel

### Erreur 401 / Authentification échouée
→ Ton token NPSSO a expiré, récupère-en un nouveau

### Le widget ne se met pas à jour
→ Vérifie l'intervalle de rafraîchissement dans Widgy
→ Vérifie que l'URL est correcte

### Données manquantes ou incorrectes
→ Assure-toi que ton profil PSN est public
→ Attends quelques minutes, les stats PSN peuvent prendre du temps à se synchroniser

## 📝 Notes importantes

- Le token NPSSO expire après environ 2 mois
- Limite de requêtes Vercel gratuit : 100GB/mois (largement suffisant)
- Les données sont récupérées en temps réel depuis PlayStation Network
- Ton token NPSSO est sensible : ne le partage jamais !

## 🆘 Besoin d'aide ?

Si ça ne fonctionne pas :
1. Vérifie que tous les fichiers sont bien uploadés sur GitHub
2. Regarde les logs dans le dashboard Vercel (section "Deployments" → "Functions")
3. Teste l'URL directement dans ton navigateur pour voir le JSON

Bon widget ! 🎮
