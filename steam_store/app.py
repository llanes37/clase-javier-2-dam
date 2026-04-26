# =========================================================================================
#  🎮 STEAM STORE CLONE - Tienda de Videojuegos con Flask
#  ────────────────────────────────────────────────────────────────────────────────────────
#  📘 Proyecto didáctico basado en la Sección 5:
#    * Listas de diccionarios para el catálogo de juegos
#    * Ordenación con key/lambda para filtros y ordenamiento
#    * min/max/sum para estadísticas y precios
#    * Comprensiones para filtrado dinámico
#    * CRUD completo con Flask y Bootstrap
#
#  🎨 Inspirado en: https://store.steampowered.com/
# =========================================================================================

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'steam_store_secret_key_2024'

# =========================================================================================
#  📊 BASE DE DATOS EN MEMORIA (Listas de Diccionarios - Sección 5)
# =========================================================================================

# * Catálogo de juegos - Lista de diccionarios con key/lambda para ordenación
catalogo_juegos = [
    {
        "id": 1,
        "nombre": "Cyberpunk 2077",
        "descripcion": "Un RPG de mundo abierto ambientado en Night City, una megalópolis obsesionada con el poder, el glamour y la modificación corporal.",
        "descripcion_corta": "RPG de mundo abierto en Night City",
        "precio": 59.99,
        "precio_original": 59.99,
        "descuento": 0,
        "categoria": "RPG",
        "desarrollador": "CD Projekt Red",
        "editor": "CD Projekt",
        "fecha_lanzamiento": "2020-12-10",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/1091500/header.jpg",
        "capturas": [
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1091500/ss_b529b0abc43f55fc23fe8058eddb6e37c9629a6a.jpg",
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1091500/ss_872822c5e50dc71f345416098d29fc3ae5cd26c1.jpg"
        ],
        "video": "https://www.youtube.com/embed/8X2kIfS6fb8",
        "etiquetas": ["RPG", "Mundo Abierto", "Cyberpunk", "Futurista", "Acción"],
        "requisitos_minimos": {"os": "Windows 10", "cpu": "Intel Core i5-3570K", "ram": "8 GB", "gpu": "GTX 970"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i7-4790", "ram": "12 GB", "gpu": "RTX 2060"},
        "valoracion": 4.2,
        "num_reviews": 458632,
        "positivas": 78,
        "plataformas": ["windows", "playstation", "xbox"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Italiano"],
        "multijugador": False,
        "logros": 44,
        "destacado": True
    },
    {
        "id": 2,
        "nombre": "The Witcher 3: Wild Hunt",
        "descripcion": "Eres Geralt de Rivia, un cazador de monstruos. Emprende una épica aventura en un mundo abierto devastado por la guerra.",
        "descripcion_corta": "La obra maestra de CD Projekt Red",
        "precio": 9.99,
        "precio_original": 39.99,
        "descuento": 75,
        "categoria": "RPG",
        "desarrollador": "CD Projekt Red",
        "editor": "CD Projekt",
        "fecha_lanzamiento": "2015-05-18",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/292030/header.jpg",
        "capturas": [
            "https://cdn.cloudflare.steamstatic.com/steam/apps/292030/ss_107600c1337accc09104f7a8aa7f275f23cad096.jpg",
            "https://cdn.cloudflare.steamstatic.com/steam/apps/292030/ss_64eb760f9a2b67f6731a71cce3a8fb684b9af267.jpg"
        ],
        "video": "https://www.youtube.com/embed/c0i88t0Kacs",
        "etiquetas": ["RPG", "Mundo Abierto", "Fantasía", "Historia Rica", "Aventura"],
        "requisitos_minimos": {"os": "Windows 7", "cpu": "Intel Core i5-2500K", "ram": "6 GB", "gpu": "GTX 660"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i7-3770", "ram": "8 GB", "gpu": "GTX 770"},
        "valoracion": 4.9,
        "num_reviews": 625841,
        "positivas": 97,
        "plataformas": ["windows", "playstation", "xbox", "nintendo"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Polaco"],
        "multijugador": False,
        "logros": 78,
        "destacado": True
    },
    {
        "id": 3,
        "nombre": "Elden Ring",
        "descripcion": "EL NUEVO RPG DE ACCIÓN DE FANTASÍA. Álzate, Sinluz, y que la gracia te guíe para abrazar el poder del Círculo de Elden.",
        "descripcion_corta": "El épico RPG de FromSoftware",
        "precio": 59.99,
        "precio_original": 59.99,
        "descuento": 0,
        "categoria": "RPG",
        "desarrollador": "FromSoftware",
        "editor": "Bandai Namco",
        "fecha_lanzamiento": "2022-02-25",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/1245620/header.jpg",
        "capturas": [
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1245620/ss_e80a907c2c43337e53316c71555c3c3035a1343e.jpg",
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1245620/ss_c372274833ae6e5437b952fa1979430546a43ad9.jpg"
        ],
        "video": "https://www.youtube.com/embed/E3Huy2cdih0",
        "etiquetas": ["Souls-like", "RPG", "Mundo Abierto", "Difícil", "Fantasía Oscura"],
        "requisitos_minimos": {"os": "Windows 10", "cpu": "Intel Core i5-8400", "ram": "12 GB", "gpu": "GTX 1060"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i7-8700K", "ram": "16 GB", "gpu": "RTX 2070"},
        "valoracion": 4.7,
        "num_reviews": 524789,
        "positivas": 92,
        "plataformas": ["windows", "playstation", "xbox"],
        "idiomas": ["Español", "Inglés", "Japonés", "Francés", "Alemán"],
        "multijugador": True,
        "logros": 42,
        "destacado": True
    },
    {
        "id": 4,
        "nombre": "Red Dead Redemption 2",
        "descripcion": "América, 1899. Arthur Morgan y la banda de Van der Linde deben huir del país. Con agentes federales pisándoles los talones.",
        "descripcion_corta": "La épica del Salvaje Oeste",
        "precio": 29.99,
        "precio_original": 59.99,
        "descuento": 50,
        "categoria": "Acción",
        "desarrollador": "Rockstar Games",
        "editor": "Rockstar Games",
        "fecha_lanzamiento": "2019-12-05",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/1174180/header.jpg",
        "capturas": [
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1174180/ss_66b553f4c209476d3e4ce25fa4714c687571d73e.jpg",
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1174180/ss_d1a8f5a69155c3186c65d1da90491fcfd43663d9.jpg"
        ],
        "video": "https://www.youtube.com/embed/eaW0tYpxyp0",
        "etiquetas": ["Mundo Abierto", "Western", "Acción", "Historia Rica", "Multijugador"],
        "requisitos_minimos": {"os": "Windows 7", "cpu": "Intel Core i5-2500K", "ram": "8 GB", "gpu": "GTX 770"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i7-4770K", "ram": "12 GB", "gpu": "RTX 2060"},
        "valoracion": 4.6,
        "num_reviews": 389654,
        "positivas": 89,
        "plataformas": ["windows", "playstation", "xbox"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Italiano"],
        "multijugador": True,
        "logros": 52,
        "destacado": True
    },
    {
        "id": 5,
        "nombre": "Counter-Strike 2",
        "descripcion": "Counter-Strike 2 es la mayor renovación técnica de la historia de CS, garantizando nuevas características y actualizaciones.",
        "descripcion_corta": "El shooter competitivo definitivo",
        "precio": 0,
        "precio_original": 0,
        "descuento": 0,
        "categoria": "FPS",
        "desarrollador": "Valve",
        "editor": "Valve",
        "fecha_lanzamiento": "2023-09-27",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg",
        "capturas": [
            "https://cdn.cloudflare.steamstatic.com/steam/apps/730/ss_d196d945c6170e9cadce3c99c5eb606e27012d3a.jpg"
        ],
        "video": "https://www.youtube.com/embed/c80dVYcL69E",
        "etiquetas": ["FPS", "Competitivo", "Multijugador", "Táctico", "E-Sports"],
        "requisitos_minimos": {"os": "Windows 10", "cpu": "Intel Core i5-3470", "ram": "8 GB", "gpu": "GTX 650"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i7", "ram": "16 GB", "gpu": "RTX 2060"},
        "valoracion": 4.3,
        "num_reviews": 987456,
        "positivas": 85,
        "plataformas": ["windows"],
        "idiomas": ["Español", "Inglés", "Ruso", "Chino", "Portugués"],
        "multijugador": True,
        "logros": 167,
        "destacado": False
    },
    {
        "id": 6,
        "nombre": "Baldur's Gate 3",
        "descripcion": "Reúne a tu grupo y regresa a los Reinos Olvidados en una historia de compañerismo y traición, supervivencia y sacrificio.",
        "descripcion_corta": "RPG del año - Juego del Año 2023",
        "precio": 59.99,
        "precio_original": 59.99,
        "descuento": 0,
        "categoria": "RPG",
        "desarrollador": "Larian Studios",
        "editor": "Larian Studios",
        "fecha_lanzamiento": "2023-08-03",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/1086940/header.jpg",
        "capturas": [
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1086940/ss_c73bc54415178c07dce5e47e8db8cf4c3a4d6e7f.jpg"
        ],
        "video": "https://www.youtube.com/embed/1T22wNvNBsY",
        "etiquetas": ["RPG", "Fantasía", "Por Turnos", "Cooperativo", "D&D"],
        "requisitos_minimos": {"os": "Windows 10", "cpu": "Intel Core i5-4690", "ram": "8 GB", "gpu": "GTX 970"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i7-8700K", "ram": "16 GB", "gpu": "RTX 2060"},
        "valoracion": 4.9,
        "num_reviews": 456123,
        "positivas": 96,
        "plataformas": ["windows", "playstation", "macos"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Italiano"],
        "multijugador": True,
        "logros": 54,
        "destacado": True
    },
    {
        "id": 7,
        "nombre": "Hogwarts Legacy",
        "descripcion": "Vive en Hogwarts en el siglo XIX. Tu personaje posee la clave de un antiguo secreto que amenaza con destruir el mundo mágico.",
        "descripcion_corta": "Tu aventura en el mundo mágico",
        "precio": 35.99,
        "precio_original": 59.99,
        "descuento": 40,
        "categoria": "RPG",
        "desarrollador": "Avalanche Software",
        "editor": "Warner Bros.",
        "fecha_lanzamiento": "2023-02-10",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/990080/header.jpg",
        "capturas": [
            "https://cdn.cloudflare.steamstatic.com/steam/apps/990080/ss_1d7a45e44faecd0ffd5c82d7b8ec0c8c8c0c8c8c.jpg"
        ],
        "video": "https://www.youtube.com/embed/BtyBjOW8sGY",
        "etiquetas": ["RPG", "Mundo Abierto", "Magia", "Fantasía", "Aventura"],
        "requisitos_minimos": {"os": "Windows 10", "cpu": "Intel Core i5-6600", "ram": "16 GB", "gpu": "GTX 960"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i7-8700", "ram": "32 GB", "gpu": "RTX 2080"},
        "valoracion": 4.5,
        "num_reviews": 245789,
        "positivas": 88,
        "plataformas": ["windows", "playstation", "xbox", "nintendo"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Japonés"],
        "multijugador": False,
        "logros": 46,
        "destacado": True
    },
    {
        "id": 8,
        "nombre": "Stardew Valley",
        "descripcion": "Has heredado la vieja granja de tu abuelo en Stardew Valley. Equípate con herramientas de segunda mano y unas monedas.",
        "descripcion_corta": "Simulador de granja relajante",
        "precio": 7.49,
        "precio_original": 14.99,
        "descuento": 50,
        "categoria": "Simulación",
        "desarrollador": "ConcernedApe",
        "editor": "ConcernedApe",
        "fecha_lanzamiento": "2016-02-26",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/413150/header.jpg",
        "capturas": [
            "https://cdn.cloudflare.steamstatic.com/steam/apps/413150/ss_64d942a86eb82e8d8c79e2e5c6d0f2e5c6d0f2e5.jpg"
        ],
        "video": "https://www.youtube.com/embed/ot7uXNQskhs",
        "etiquetas": ["Simulación", "Granja", "Pixel Art", "Relajante", "Cooperativo"],
        "requisitos_minimos": {"os": "Windows Vista", "cpu": "2 GHz", "ram": "2 GB", "gpu": "256 MB"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "2.8 GHz", "ram": "4 GB", "gpu": "512 MB"},
        "valoracion": 4.9,
        "num_reviews": 456789,
        "positivas": 98,
        "plataformas": ["windows", "macos", "linux", "playstation", "xbox", "nintendo"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Chino"],
        "multijugador": True,
        "logros": 40,
        "destacado": False
    },
    {
        "id": 9,
        "nombre": "Hades",
        "descripcion": "Desafía al dios de los muertos mientras luchas para salir del Inframundo en este juego rogue-like de los creadores de Bastion.",
        "descripcion_corta": "Rogue-like mitológico",
        "precio": 12.49,
        "precio_original": 24.99,
        "descuento": 50,
        "categoria": "Roguelike",
        "desarrollador": "Supergiant Games",
        "editor": "Supergiant Games",
        "fecha_lanzamiento": "2020-09-17",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/1145360/header.jpg",
        "capturas": [
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1145360/ss_c7f3d6d0f2e5c6d0f2e5c6d0f2e5c6d0f2e5c6d0.jpg"
        ],
        "video": "https://www.youtube.com/embed/91t0ha9x0AE",
        "etiquetas": ["Roguelike", "Acción", "Mitología", "Indie", "Hack and Slash"],
        "requisitos_minimos": {"os": "Windows 7", "cpu": "Dual Core 2.4 GHz", "ram": "4 GB", "gpu": "GTX 560"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Dual Core 3.0 GHz", "ram": "8 GB", "gpu": "GTX 1060"},
        "valoracion": 4.8,
        "num_reviews": 234567,
        "positivas": 95,
        "plataformas": ["windows", "macos", "playstation", "xbox", "nintendo"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Italiano"],
        "multijugador": False,
        "logros": 49,
        "destacado": True
    },
    {
        "id": 10,
        "nombre": "Minecraft",
        "descripcion": "Explora mundos infinitos y construye desde casas hasta grandes ciudades. Sobrevive en modo survival o crea en modo creativo.",
        "descripcion_corta": "El juego de construcción más vendido",
        "precio": 26.95,
        "precio_original": 26.95,
        "descuento": 0,
        "categoria": "Sandbox",
        "desarrollador": "Mojang Studios",
        "editor": "Xbox Game Studios",
        "fecha_lanzamiento": "2011-11-18",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/1672970/header.jpg",
        "capturas": [],
        "video": "https://www.youtube.com/embed/MmB9b5njVbA",
        "etiquetas": ["Sandbox", "Construcción", "Supervivencia", "Multijugador", "Creatividad"],
        "requisitos_minimos": {"os": "Windows 10", "cpu": "Intel Core i3-3210", "ram": "4 GB", "gpu": "Intel HD 4000"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i5-4690", "ram": "8 GB", "gpu": "GTX 700"},
        "valoracion": 4.7,
        "num_reviews": 123456,
        "positivas": 93,
        "plataformas": ["windows", "macos", "linux", "playstation", "xbox", "nintendo", "mobile"],
        "idiomas": ["Español", "Inglés", "Todos los idiomas"],
        "multijugador": True,
        "logros": 80,
        "destacado": False
    },
    {
        "id": 11,
        "nombre": "God of War",
        "descripcion": "Kratos ya no es un simple guerrero. Como padre y mentor, debe controlar su ira y guiar a su hijo por un mundo peligroso.",
        "descripcion_corta": "La saga nórdica de Kratos",
        "precio": 29.99,
        "precio_original": 49.99,
        "descuento": 40,
        "categoria": "Acción",
        "desarrollador": "Santa Monica Studio",
        "editor": "PlayStation Studios",
        "fecha_lanzamiento": "2022-01-14",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/1593500/header.jpg",
        "capturas": [],
        "video": "https://www.youtube.com/embed/K0u_kAWLJOA",
        "etiquetas": ["Acción", "Aventura", "Mitología", "Historia Rica", "Hack and Slash"],
        "requisitos_minimos": {"os": "Windows 10", "cpu": "Intel Core i5-2500K", "ram": "8 GB", "gpu": "GTX 960"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i7-4770K", "ram": "16 GB", "gpu": "RTX 2060"},
        "valoracion": 4.8,
        "num_reviews": 156789,
        "positivas": 97,
        "plataformas": ["windows", "playstation"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Italiano"],
        "multijugador": False,
        "logros": 36,
        "destacado": True
    },
    {
        "id": 12,
        "nombre": "Hollow Knight",
        "descripcion": "Desciende a las profundidades de Hallownest, un vasto y retorcido reino subterráneo de insectos y héroes.",
        "descripcion_corta": "Metroidvania indie masterpiece",
        "precio": 7.49,
        "precio_original": 14.99,
        "descuento": 50,
        "categoria": "Metroidvania",
        "desarrollador": "Team Cherry",
        "editor": "Team Cherry",
        "fecha_lanzamiento": "2017-02-24",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/367520/header.jpg",
        "capturas": [],
        "video": "https://www.youtube.com/embed/UAO2urG23S4",
        "etiquetas": ["Metroidvania", "Indie", "Difícil", "Plataformas", "Atmosférico"],
        "requisitos_minimos": {"os": "Windows 7", "cpu": "Intel Core 2 Duo E5200", "ram": "4 GB", "gpu": "GeForce 9800"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i5", "ram": "8 GB", "gpu": "GTX 560"},
        "valoracion": 4.9,
        "num_reviews": 345678,
        "positivas": 97,
        "plataformas": ["windows", "macos", "linux", "playstation", "xbox", "nintendo"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Italiano"],
        "multijugador": False,
        "logros": 63,
        "destacado": False
    },
    {
        "id": 13,
        "nombre": "FIFA 24",
        "descripcion": "EA SPORTS FC™ 24 es un nuevo capítulo para el fútbol, con más de 19.000 jugadores, 700+ equipos y 30+ ligas.",
        "descripcion_corta": "El simulador de fútbol más realista",
        "precio": 41.99,
        "precio_original": 69.99,
        "descuento": 40,
        "categoria": "Deportes",
        "desarrollador": "EA Sports",
        "editor": "Electronic Arts",
        "fecha_lanzamiento": "2023-09-29",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/2195250/header.jpg",
        "capturas": [],
        "video": "https://www.youtube.com/embed/vCwS9rZ_ezI",
        "etiquetas": ["Deportes", "Fútbol", "Multijugador", "Competitivo", "Simulación"],
        "requisitos_minimos": {"os": "Windows 10", "cpu": "Intel Core i5-6600K", "ram": "8 GB", "gpu": "GTX 1050 Ti"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i7-6700", "ram": "12 GB", "gpu": "RTX 2060"},
        "valoracion": 3.2,
        "num_reviews": 89456,
        "positivas": 42,
        "plataformas": ["windows", "playstation", "xbox", "nintendo"],
        "idiomas": ["Español", "Inglés", "Todos los idiomas"],
        "multijugador": True,
        "logros": 42,
        "destacado": False
    },
    {
        "id": 14,
        "nombre": "Resident Evil 4 Remake",
        "descripcion": "Sobrevive al horror. Seis años después de los sucesos de Raccoon City, Leon S. Kennedy es enviado a rescatar a la hija del presidente.",
        "descripcion_corta": "El remake del clásico de terror",
        "precio": 35.99,
        "precio_original": 59.99,
        "descuento": 40,
        "categoria": "Terror",
        "desarrollador": "Capcom",
        "editor": "Capcom",
        "fecha_lanzamiento": "2023-03-24",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/2050650/header.jpg",
        "capturas": [],
        "video": "https://www.youtube.com/embed/E_Fk2GxKwE0",
        "etiquetas": ["Terror", "Survival Horror", "Acción", "Zombies", "Remake"],
        "requisitos_minimos": {"os": "Windows 10", "cpu": "Intel Core i5-8400", "ram": "12 GB", "gpu": "GTX 1060"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i7-8700", "ram": "16 GB", "gpu": "RTX 2070"},
        "valoracion": 4.7,
        "num_reviews": 187654,
        "positivas": 96,
        "plataformas": ["windows", "playstation", "xbox"],
        "idiomas": ["Español", "Inglés", "Japonés", "Francés", "Alemán"],
        "multijugador": False,
        "logros": 39,
        "destacado": True
    },
    {
        "id": 15,
        "nombre": "Terraria",
        "descripcion": "Cava, lucha, explora, construye. Nada es imposible en este juego de aventuras lleno de acción. El mundo es tu lienzo.",
        "descripcion_corta": "Aventura sandbox 2D",
        "precio": 4.99,
        "precio_original": 9.99,
        "descuento": 50,
        "categoria": "Sandbox",
        "desarrollador": "Re-Logic",
        "editor": "Re-Logic",
        "fecha_lanzamiento": "2011-05-16",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/105600/header.jpg",
        "capturas": [],
        "video": "https://www.youtube.com/embed/w7uOhFTrrq0",
        "etiquetas": ["Sandbox", "Aventura", "Supervivencia", "Cooperativo", "2D"],
        "requisitos_minimos": {"os": "Windows XP", "cpu": "2.0 GHz", "ram": "2.5 GB", "gpu": "256 MB"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "2.5 GHz", "ram": "4 GB", "gpu": "512 MB"},
        "valoracion": 4.9,
        "num_reviews": 876543,
        "positivas": 98,
        "plataformas": ["windows", "macos", "linux", "playstation", "xbox", "nintendo", "mobile"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Italiano"],
        "multijugador": True,
        "logros": 104,
        "destacado": False
    },
    {
        "id": 16,
        "nombre": "Grand Theft Auto V",
        "descripcion": "Los Santos: una metrópolis en expansión llena de estrellas de autoayuda, actores venidos a menos y reality shows.",
        "descripcion_corta": "El sandbox criminal definitivo",
        "precio": 14.99,
        "precio_original": 29.99,
        "descuento": 50,
        "categoria": "Acción",
        "desarrollador": "Rockstar North",
        "editor": "Rockstar Games",
        "fecha_lanzamiento": "2015-04-14",
        "imagen": "https://cdn.cloudflare.steamstatic.com/steam/apps/271590/header.jpg",
        "capturas": [],
        "video": "https://www.youtube.com/embed/QkkoHAzjnUs",
        "etiquetas": ["Mundo Abierto", "Acción", "Crimen", "Multijugador", "Conducción"],
        "requisitos_minimos": {"os": "Windows 8.1", "cpu": "Intel Core 2 Quad Q6600", "ram": "4 GB", "gpu": "GTX 660"},
        "requisitos_recomendados": {"os": "Windows 10", "cpu": "Intel Core i5-3470", "ram": "8 GB", "gpu": "GTX 1060"},
        "valoracion": 4.5,
        "num_reviews": 1245678,
        "positivas": 88,
        "plataformas": ["windows", "playstation", "xbox"],
        "idiomas": ["Español", "Inglés", "Francés", "Alemán", "Italiano"],
        "multijugador": True,
        "logros": 77,
        "destacado": True
    }
]

# * Categorías disponibles - Diccionario con listas
categorias = {
    "Todos": "Todos los juegos",
    "RPG": "Juegos de rol",
    "FPS": "Shooters en primera persona",
    "Acción": "Juegos de acción",
    "Aventura": "Juegos de aventura",
    "Simulación": "Simuladores",
    "Deportes": "Juegos deportivos",
    "Terror": "Juegos de terror",
    "Roguelike": "Rogue-likes y Rogue-lites",
    "Metroidvania": "Metroidvanias",
    "Sandbox": "Juegos sandbox",
    "Indie": "Juegos independientes"
}

# * Carrito de compras - Lista de diccionarios
carrito_global = []
carrito_contador = 0

# * Lista de deseos (Wishlist)
wishlist_global = []

# * Biblioteca de juegos comprados
biblioteca_global = []

# * Reviews de usuarios
reviews_global = []
review_contador = 0

# =========================================================================================
#  🔧 FUNCIONES AUXILIARES (Usando conceptos de Sección 5)
# =========================================================================================

def obtener_juego_por_id(id_juego):
    """Buscar juego por ID usando comprensión de listas"""
    juegos = [j for j in catalogo_juegos if j["id"] == id_juego]
    return juegos[0] if juegos else None

def filtrar_por_categoria(categoria):
    """Filtrar juegos por categoría usando comprensión"""
    if categoria == "Todos":
        return catalogo_juegos
    return [j for j in catalogo_juegos if j["categoria"] == categoria]

def filtrar_por_precio(juegos, min_precio=0, max_precio=float('inf')):
    """Filtrar por rango de precios"""
    return [j for j in juegos if min_precio <= j["precio"] <= max_precio]

def filtrar_ofertas(juegos):
    """Obtener juegos con descuento"""
    return [j for j in juegos if j["descuento"] > 0]

def filtrar_gratis(juegos):
    """Obtener juegos gratis"""
    return [j for j in juegos if j["precio"] == 0]

def ordenar_juegos(juegos, criterio="nombre", descendente=False):
    """Ordenar usando sorted() con key lambda - Sección 5"""
    criterios_validos = {
        "nombre": lambda j: j["nombre"].lower(),
        "precio": lambda j: j["precio"],
        "valoracion": lambda j: j["valoracion"],
        "descuento": lambda j: j["descuento"],
        "fecha": lambda j: j["fecha_lanzamiento"],
        "reviews": lambda j: j["num_reviews"]
    }
    key_func = criterios_validos.get(criterio, lambda j: j["nombre"].lower())
    return sorted(juegos, key=key_func, reverse=descendente)

def buscar_juegos(query):
    """Búsqueda por nombre o etiquetas"""
    query = query.lower()
    return [
        j for j in catalogo_juegos
        if query in j["nombre"].lower() or
           any(query in et.lower() for et in j["etiquetas"])
    ]

def obtener_estadisticas():
    """Estadísticas usando min/max/sum - Sección 5"""
    precios = [j["precio"] for j in catalogo_juegos if j["precio"] > 0]
    return {
        "total_juegos": len(catalogo_juegos),
        "precio_mas_bajo": min(precios) if precios else 0,
        "precio_mas_alto": max(precios) if precios else 0,
        "precio_promedio": round(sum(precios) / len(precios), 2) if precios else 0,
        "juegos_gratis": len([j for j in catalogo_juegos if j["precio"] == 0]),
        "juegos_con_descuento": len([j for j in catalogo_juegos if j["descuento"] > 0]),
        "mejor_valorado": max(catalogo_juegos, key=lambda j: j["valoracion"])["nombre"],
        "mas_reseñas": max(catalogo_juegos, key=lambda j: j["num_reviews"])["nombre"]
    }

def calcular_total_carrito():
    """Calcular total del carrito con sum()"""
    return round(sum(item["precio"] * item["cantidad"] for item in carrito_global), 2)

def calcular_ahorro_carrito():
    """Calcular ahorro total"""
    return round(sum(
        (item["precio_original"] - item["precio"]) * item["cantidad"]
        for item in carrito_global
    ), 2)

# =========================================================================================
#  🌐 RUTAS DE LA APLICACIÓN
# =========================================================================================

@app.route('/')
def index():
    """Página principal con destacados y ofertas"""
    # Juegos destacados usando comprensión
    destacados = [j for j in catalogo_juegos if j.get("destacado", False)]
    
    # Mejores ofertas - ordenar por descuento descendente
    ofertas = sorted(
        [j for j in catalogo_juegos if j["descuento"] > 0],
        key=lambda j: j["descuento"],
        reverse=True
    )[:6]
    
    # Mejor valorados
    mejor_valorados = sorted(
        catalogo_juegos,
        key=lambda j: j["valoracion"],
        reverse=True
    )[:6]
    
    # Nuevos lanzamientos
    nuevos = sorted(
        catalogo_juegos,
        key=lambda j: j["fecha_lanzamiento"],
        reverse=True
    )[:6]
    
    # Juegos gratis
    gratis = [j for j in catalogo_juegos if j["precio"] == 0]
    
    # Estadísticas
    stats = obtener_estadisticas()
    
    return render_template('index.html',
                         destacados=destacados,
                         ofertas=ofertas,
                         mejor_valorados=mejor_valorados,
                         nuevos=nuevos,
                         gratis=gratis,
                         stats=stats,
                         categorias=categorias,
                         carrito_count=len(carrito_global))

@app.route('/tienda')
def tienda():
    """Catálogo de juegos con filtros"""
    # Obtener parámetros de filtrado
    categoria = request.args.get('categoria', 'Todos')
    orden = request.args.get('orden', 'nombre')
    direccion = request.args.get('direccion', 'asc')
    precio_min = float(request.args.get('precio_min', 0))
    precio_max = float(request.args.get('precio_max', 999))
    busqueda = request.args.get('q', '')
    solo_ofertas = request.args.get('ofertas', '') == 'true'
    solo_gratis = request.args.get('gratis', '') == 'true'
    
    # Aplicar filtros usando comprensiones - Sección 5
    juegos = catalogo_juegos.copy()
    
    if busqueda:
        juegos = buscar_juegos(busqueda)
    elif categoria != 'Todos':
        juegos = filtrar_por_categoria(categoria)
    
    juegos = filtrar_por_precio(juegos, precio_min, precio_max)
    
    if solo_ofertas:
        juegos = filtrar_ofertas(juegos)
    
    if solo_gratis:
        juegos = filtrar_gratis(juegos)
    
    # Ordenar usando sorted con key - Sección 5
    juegos = ordenar_juegos(juegos, orden, direccion == 'desc')
    
    return render_template('tienda.html',
                         juegos=juegos,
                         categorias=categorias,
                         categoria_actual=categoria,
                         orden_actual=orden,
                         direccion_actual=direccion,
                         busqueda=busqueda,
                         total_resultados=len(juegos),
                         carrito_count=len(carrito_global))

@app.route('/juego/<int:id>')
def detalle_juego(id):
    """Página de detalle del juego"""
    juego = obtener_juego_por_id(id)
    if not juego:
        return render_template('404.html'), 404
    
    # Juegos similares (misma categoría)
    similares = [j for j in catalogo_juegos 
                 if j["categoria"] == juego["categoria"] and j["id"] != id][:4]
    
    # Reviews del juego
    reviews_juego = [r for r in reviews_global if r["juego_id"] == id]
    
    # Verificar si está en carrito o wishlist
    en_carrito = any(item["id"] == id for item in carrito_global)
    en_wishlist = any(item["id"] == id for item in wishlist_global)
    en_biblioteca = any(item["id"] == id for item in biblioteca_global)
    
    return render_template('detalle_juego.html',
                         juego=juego,
                         similares=similares,
                         reviews=reviews_juego,
                         en_carrito=en_carrito,
                         en_wishlist=en_wishlist,
                         en_biblioteca=en_biblioteca,
                         categorias=categorias,
                         carrito_count=len(carrito_global))

@app.route('/carrito')
def ver_carrito():
    """Ver carrito de compras"""
    total = calcular_total_carrito()
    ahorro = calcular_ahorro_carrito()
    
    return render_template('carrito.html',
                         carrito=carrito_global,
                         total=total,
                         ahorro=ahorro,
                         categorias=categorias,
                         carrito_count=len(carrito_global))

@app.route('/biblioteca')
def biblioteca():
    """Biblioteca de juegos comprados"""
    return render_template('biblioteca.html',
                         biblioteca=biblioteca_global,
                         categorias=categorias,
                         carrito_count=len(carrito_global))

@app.route('/wishlist')
def ver_wishlist():
    """Lista de deseos"""
    return render_template('wishlist.html',
                         wishlist=wishlist_global,
                         categorias=categorias,
                         carrito_count=len(carrito_global))

# =========================================================================================
#  🔌 API REST
# =========================================================================================

@app.route('/api/juegos')
def api_juegos():
    """API: Obtener todos los juegos"""
    categoria = request.args.get('categoria', 'Todos')
    orden = request.args.get('orden', 'nombre')
    
    juegos = filtrar_por_categoria(categoria)
    juegos = ordenar_juegos(juegos, orden)
    
    return jsonify({
        "success": True,
        "total": len(juegos),
        "juegos": juegos
    })

@app.route('/api/juego/<int:id>')
def api_juego(id):
    """API: Obtener un juego por ID"""
    juego = obtener_juego_por_id(id)
    if juego:
        return jsonify({"success": True, "juego": juego})
    return jsonify({"success": False, "error": "Juego no encontrado"}), 404

@app.route('/api/carrito', methods=['GET'])
def api_carrito_get():
    """API: Obtener carrito"""
    return jsonify({
        "success": True,
        "carrito": carrito_global,
        "total": calcular_total_carrito(),
        "ahorro": calcular_ahorro_carrito(),
        "cantidad_items": len(carrito_global)
    })

@app.route('/api/carrito/agregar', methods=['POST'])
def api_carrito_agregar():
    """API: Agregar juego al carrito"""
    global carrito_contador
    data = request.json
    id_juego = data.get('id')
    
    juego = obtener_juego_por_id(id_juego)
    if not juego:
        return jsonify({"success": False, "error": "Juego no encontrado"}), 404
    
    # Verificar si ya está en el carrito
    for item in carrito_global:
        if item["id"] == id_juego:
            item["cantidad"] += 1
            return jsonify({
                "success": True,
                "message": f"Cantidad actualizada: {item['cantidad']}",
                "carrito_count": len(carrito_global)
            })
    
    # Agregar nuevo item
    carrito_contador += 1
    item_carrito = {
        "carrito_id": carrito_contador,
        "id": juego["id"],
        "nombre": juego["nombre"],
        "imagen": juego["imagen"],
        "precio": juego["precio"],
        "precio_original": juego["precio_original"],
        "descuento": juego["descuento"],
        "cantidad": 1
    }
    carrito_global.append(item_carrito)
    
    return jsonify({
        "success": True,
        "message": f"'{juego['nombre']}' agregado al carrito",
        "carrito_count": len(carrito_global)
    })

@app.route('/api/carrito/eliminar/<int:id>', methods=['DELETE'])
def api_carrito_eliminar(id):
    """API: Eliminar juego del carrito"""
    global carrito_global
    carrito_global = [item for item in carrito_global if item["id"] != id]
    
    return jsonify({
        "success": True,
        "message": "Juego eliminado del carrito",
        "carrito_count": len(carrito_global),
        "total": calcular_total_carrito()
    })

@app.route('/api/carrito/vaciar', methods=['DELETE'])
def api_carrito_vaciar():
    """API: Vaciar carrito"""
    global carrito_global
    carrito_global = []
    
    return jsonify({
        "success": True,
        "message": "Carrito vaciado",
        "carrito_count": 0
    })

@app.route('/api/carrito/comprar', methods=['POST'])
def api_carrito_comprar():
    """API: Procesar compra"""
    global carrito_global, biblioteca_global
    
    if not carrito_global:
        return jsonify({"success": False, "error": "El carrito está vacío"}), 400
    
    # Agregar juegos a biblioteca
    for item in carrito_global:
        if not any(j["id"] == item["id"] for j in biblioteca_global):
            biblioteca_global.append({
                "id": item["id"],
                "nombre": item["nombre"],
                "imagen": item["imagen"],
                "fecha_compra": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "tiempo_jugado": 0
            })
    
    total_compra = calcular_total_carrito()
    juegos_comprados = len(carrito_global)
    carrito_global = []
    
    return jsonify({
        "success": True,
        "message": f"¡Compra realizada! {juegos_comprados} juego(s) añadidos a tu biblioteca",
        "total_pagado": total_compra,
        "carrito_count": 0
    })

@app.route('/api/wishlist/agregar', methods=['POST'])
def api_wishlist_agregar():
    """API: Agregar a lista de deseos"""
    data = request.json
    id_juego = data.get('id')
    
    juego = obtener_juego_por_id(id_juego)
    if not juego:
        return jsonify({"success": False, "error": "Juego no encontrado"}), 404
    
    if any(j["id"] == id_juego for j in wishlist_global):
        return jsonify({"success": False, "error": "Ya está en tu lista de deseos"}), 400
    
    wishlist_global.append({
        "id": juego["id"],
        "nombre": juego["nombre"],
        "imagen": juego["imagen"],
        "precio": juego["precio"],
        "precio_original": juego["precio_original"],
        "descuento": juego["descuento"],
        "fecha_agregado": datetime.now().strftime("%Y-%m-%d")
    })
    
    return jsonify({
        "success": True,
        "message": f"'{juego['nombre']}' añadido a lista de deseos"
    })

@app.route('/api/wishlist/eliminar/<int:id>', methods=['DELETE'])
def api_wishlist_eliminar(id):
    """API: Eliminar de lista de deseos"""
    global wishlist_global
    wishlist_global = [j for j in wishlist_global if j["id"] != id]
    
    return jsonify({"success": True, "message": "Eliminado de lista de deseos"})

@app.route('/api/review', methods=['POST'])
def api_agregar_review():
    """API: Agregar review"""
    global review_contador
    data = request.json
    
    review_contador += 1
    review = {
        "id": review_contador,
        "juego_id": data.get('juego_id'),
        "usuario": data.get('usuario', 'Usuario Anónimo'),
        "valoracion": data.get('valoracion', 5),
        "contenido": data.get('contenido', ''),
        "recomendado": data.get('recomendado', True),
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "horas_jugadas": data.get('horas_jugadas', 0)
    }
    reviews_global.append(review)
    
    return jsonify({"success": True, "message": "Review añadida", "review": review})

@app.route('/api/estadisticas')
def api_estadisticas():
    """API: Estadísticas de la tienda"""
    return jsonify({
        "success": True,
        "estadisticas": obtener_estadisticas()
    })

@app.route('/api/buscar')
def api_buscar():
    """API: Búsqueda de juegos"""
    query = request.args.get('q', '')
    resultados = buscar_juegos(query) if query else []
    
    return jsonify({
        "success": True,
        "query": query,
        "resultados": len(resultados),
        "juegos": resultados
    })

# =========================================================================================
#  🚀 EJECUTAR SERVIDOR
# =========================================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🎮 STEAM STORE CLONE - Tienda de Videojuegos")
    print("=" * 60)
    print(f"📊 {len(catalogo_juegos)} juegos en el catálogo")
    print(f"📁 {len(categorias)} categorías disponibles")
    print("=" * 60)
    print("🌐 Servidor iniciando en: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
