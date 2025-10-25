"""
Lista estática de géneros musicales y helper para devolverlos.
Usar un módulo separado facilita mantenimiento y posible sincronización futura.
"""
from typing import List

def get_genres() -> List[str]:
    # Lista extensa (no exhaustiva) de géneros musicales comunes y subgéneros.
    GENRES = [
        "Pop", "Rock", "Indie", "Alternative", "Hard Rock", "Soft Rock",
        "Classic Rock", "Progressive Rock", "Punk", "Post-Punk", "Emo",
        "Metal", "Heavy Metal", "Thrash Metal", "Death Metal", "Black Metal",
        "Doom Metal", "Power Metal", "Grunge", "Blues", "Blues Rock",
        "Jazz", "Smooth Jazz", "Bebop", "Fusion", "Swing", "Soul", "R&B",
        "Funk", "Disco", "Gospel", "Christian", "Reggae", "Ska", "Dub",
        "Hip Hop", "Rap", "Trap", "Boom Bap", "Lo-fi Hip Hop", "Ragga",
        "Electronic", "EDM", "House", "Deep House", "Tech House", "Progressive House",
        "Techno", "Minimal", "Trance", "Drum and Bass", "DnB", "Jungle",
        "Ambient", "Downtempo", "Chillout", "Electro", "Synthwave", "Industrial",
        "Experimental", "Noise", "Avant-Garde", "Classical", "Baroque", "Romantic",
        "Contemporary Classical", "Opera", "Soundtrack", "Film Score", "World",
        "Latin", "Salsa", "Bachata", "Merengue", "Reggaeton", "Tango", "Flamenco",
        "Afrobeat", "Highlife", "K-Pop", "J-Pop", "C-Pop", "Mandopop", "Bollywood",
        "Folk", "Country", "Alt-Country", "Bluegrass", "Singer-Songwriter", "Acoustic",
        "Psychedelic", "House Pop", "Indie Pop", "Synth Pop", "Electropop", "Dance Pop",
        "Latin Pop", "Contemporary R&B", "Neo Soul", "Garage Rock", "Britpop",
        "Trap Metal", "Post-Rock", "Math Rock", "Ambient Pop", "New Wave",
        "Minimal Wave", "Sertanejo", "Tropical", "Cumbia", "Vallenato", "Zouk",
        "Afro-Cuban", "Flamenco Fusion", "World Fusion", "Experimental Pop",
        "Garage", "Southern Rock", "Shoegaze", "Dream Pop", "College Rock",
        "Hardcore Punk", "Metalcore", "Post-Hardcore", "Screamo",
        "Blue Eyed Soul", "Ragtime", "Traditional", "Contemporary", "Elektronica"
    ]
    # Normalizar: quitar duplicados y ordenar para presentación
    return sorted(set(GENRES))
