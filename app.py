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
    deux_semaines = timedelta(days=14)

    for nom, url in flux_list.items():
        flux = feedparser.parse(url)
        videos = []

        for entry in flux.entries:
            try:
                # Convertit la date du flux RSS en datetime
                published = datetime.fromtimestamp(time.mktime(entry.published_parsed))
            except Exception:
                continue

            # Vérifie si la vidéo date de moins de 14 jours
            if now - published <= deux_semaines:
                videos.append({
                    "titre": entry.title,
                    "lien": entry.link,
                    "date": published.strftime("%d %B %Y à %Hh%M")
                })

        resultats[nom] = videos

    return render_template("index.html", flux=resultats)

# 🚨 Important pour Render : écouter sur 0.0.0.0 et le port défini par l'env
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
