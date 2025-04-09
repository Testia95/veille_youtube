from datetime import datetime, timedelta
import time
from flask import Flask, render_template
import feedparser
import os

app = Flask(__name__)

# Liste des chaînes YouTube à surveiller (titre → flux RSS)
flux_list = {
    "Le Media": "https://www.youtube.com/feeds/videos.xml?channel_id=UCT67YOMntJxfRnO_9bXDpvw",
    "Blast": "https://www.youtube.com/feeds/videos.xml?channel_id=UC__xRB5L4toU9yYawt_lIKg",
}

@app.route("/")
def index():
    resultats = {}
    now = datetime.now()
    deux_semaines = timedelta(days=14)  # ⏳ Filtrer sur les 14 derniers jours

    for nom, url in flux_list.items():
        flux = feedparser.parse(url)
        videos = []

        for entry in flux.entries:
            try:
                # 🕒 Convertit la date RSS en objet datetime
                published = datetime.fromtimestamp(time.mktime(entry.published_parsed))
            except Exception:
                continue

            # ✅ Garde uniquement les vidéos récentes
            if now - published <= deux_semaines:
                # 🔍 Extrait l'ID de la vidéo depuis l'URL
                video_id = entry.link.split("v=")[-1]

                # 📦 Création du dictionnaire de données vidéo avec miniature + iframe
                videos.append({
                    "titre": entry.title,
                    "lien": entry.link,
                    "date": published.strftime("%d %B %Y à %Hh%M"),
                    "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                    "embed": f"https://www.youtube.com/embed/{video_id}"
                })

        # 📂 Ajoute les vidéos de la chaîne au résultat global
        resultats[nom] = videos

    # 📤 Envoie le tout au template HTML
    return render_template("index.html", flux=resultats)

# 🧠 Render impose d’utiliser son port → on le récupère depuis l’environnement
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)