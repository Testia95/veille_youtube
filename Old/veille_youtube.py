import feedparser

flux_list = {
    "Le Media": "https://www.youtube.com/feeds/videos.xml?channel_id=UCT67YOMntJxfRnO_9bXDpvw",
    "Blast": "https://www.youtube.com/feeds/videos.xml?channel_id=UC__xRB5L4toU9yYawt_lIKg",
    
}

nb_videos = 5

print("\n📺 Dernières vidéos YouTube :\n")

for nom, url in flux_list.items():
    print(f"=== {nom} ===")
    flux = feedparser.parse(url)
    
    for entry in flux.entries[:nb_videos]:
        titre = entry.title
        lien = entry.link
        date = entry.published
        print(f"- {titre}\n  {date}\n  {lien}\n")
    
    print("\n")
