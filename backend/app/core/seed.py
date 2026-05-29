"""
seed.py — Datos iniciales de NETPOLIX
======================================
Este archivo se ejecuta automáticamente al arrancar el servidor.
Es idempotente: si los datos ya existen, no los duplica.

PARA AGREGAR NUEVAS PELÍCULAS:
  Edita la lista PELICULAS al final de este archivo.
  Cada película necesita: isan, titulo_original, anio_produccion,
  duracion, imagen_url, descripcion, tipo, clasificacion_id

PARA CAMBIAR IMÁGENES/PORTADAS:
  Cambia el campo imagen_url de cada película.
  Puedes usar URLs externas o rutas locales como /static/img/nombre.jpg
"""
from decimal import Decimal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ADMIN_DATA = {
    "cedula": "1014857119",
    "nombre": "Esteban Alejandro Perez",
    "password": "Gatitoasul1",
    "is_admin": True,
}

PELICULAS = [

    {
        "isan": "0000-0000-1A2B-0000-S-0000-0003",
        "titulo_original": "The Dark Knight",
        "anio_produccion": 2008,
        "duracion": 152,
        "tipo": "Película",
        "descripcion": "Batman enfrenta al Joker, un criminal caótico que busca sumir Gotham en la anarquía total.",
        "imagen_url": "/static/img/dark_knight.webp",
        "trailer_url": "",
        "clasificacion_id": 1,
        "categorias": ["Accion"],
    },
    {
        "isan": "0000-0000-1A2B-0000-S-0000-0004",
        "titulo_original": "Parasite",
        "anio_produccion": 2019,
        "duracion": 132,
        "tipo": "Película",
        "descripcion": "Una familia sin recursos se infiltra en la vida de una familia adinerada con consecuencias imprevisibles.",
        "imagen_url": "/static/img/parasite.jpg",
        "trailer_url": "",
        "clasificacion_id": 2,
        "categorias": ["Drama", "Terror"],
    },
    {
        "isan": "0000-0000-1A2B-0000-S-0000-0005",
        "titulo_original": "Get Out",
        "anio_produccion": 2017,
        "duracion": 104,
        "tipo": "Película",
        "descripcion": "Un joven afroamericano visita a la familia de su novia y descubre secretos perturbadores.",
        "imagen_url": "/static/img/get_out.jpg",
        "trailer_url": "",
        "clasificacion_id": 2,
        "categorias": ["Terror"],
    },
    {
        "isan": "0000-0000-1A2B-0000-S-0000-0006",
        "titulo_original": "The Matrix",
        "anio_produccion": 1999,
        "duracion": 136,
        "tipo": "Película",
        "descripcion": "Un programador descubre que la realidad tal como la conoce es una simulación controlada por máquinas.",
        "imagen_url": "/static/img/matrix.webp",
        "trailer_url": "",
        "clasificacion_id": 1,
        "categorias": ["Accion", "Ciencia Ficcion"],
    },
    {
        "isan": "0000-0000-1A2B-0000-S-0000-0007",
        "titulo_original": "Pulp Fiction",
        "anio_produccion": 1994,
        "duracion": 154,
        "tipo": "Película",
        "descripcion": "Varias historias de crimen se entrecruzan en el Los Ángeles del hampa de manera no lineal.",
        "imagen_url": "/static/img/pulp_fiction.webp",
        "trailer_url": "",
        "clasificacion_id": 2,
        "categorias": ["Drama", "Accion"],
    },
    {
        "isan": "0000-0000-1A2B-0000-S-0000-0008",
        "titulo_original": "La La Land",
        "anio_produccion": 2016,
        "duracion": 128,
        "tipo": "Película",
        "descripcion": "Una actriz y un pianista de jazz se enamoran mientras persiguen sus sueños en Los Ángeles.",
        "imagen_url": "/static/img/la_la_land.webp",
        "trailer_url": "",
        "clasificacion_id": 1,
        "categorias": ["Drama", "Comedia"],
    },
    {
        "isan": "0000-0000-1A2B-0000-S-0000-0009",
        "titulo_original": "A Quiet Place",
        "anio_produccion": 2018,
        "duracion": 90,
        "tipo": "Película",
        "descripcion": "Una familia sobrevive en silencio absoluto para evitar ser detectada por criaturas que cazan por sonido.",
        "imagen_url": "/static/img/a_quiet_place.jpg",
        "trailer_url": "",
        "clasificacion_id": 2,
        "categorias": ["Terror"],
    },
    {
        "isan": "0000-0000-1A2B-0000-S-0000-0010",
        "titulo_original": "Knives Out",
        "anio_produccion": 2019,
        "duracion": 130,
        "tipo": "Película",
        "descripcion": "Un detective investiga la muerte de un famoso escritor rodeado de una familia llena de secretos.",
        "imagen_url": "/static/img/knives_out.webp",
        "trailer_url": "",
        "clasificacion_id": 1,
        "categorias": ["Comedia", "Drama"],
    },
    {
        "isan": "0000-0000-1A2B-0000-S-0000-0011",
        "titulo_original": "Everything Everywhere All at Once",
        "anio_produccion": 2022,
        "duracion": 139,
        "tipo": "Película",
        "descripcion": "Una lavandera debe conectar con versiones paralelas de sí misma para salvar el multiverso.",
        "imagen_url": "/static/img/everything_everywhere.jpg",
        "trailer_url": "",
        "clasificacion_id": 1,
        "categorias": ["Accion", "Comedia", "Ciencia Ficcion"],
    },
    {
        "isan": "0000-0000-1A2B-0000-S-0000-0012",
        "titulo_original": "Avengers: Endgame",
        "anio_produccion": 2019,
        "duracion": 181,
        "tipo": "Película",
        "descripcion": "Los Vengadores se reúnen por última vez para revertir el chasquido de Thanos y restaurar el universo.",
        "imagen_url": "/static/img/endgame.jpg",
        "trailer_url": "",
        "clasificacion_id": 1,
        "categorias": ["Accion"],
    },
]

def run_seed(db: Session):
    _crear_clasificaciones_base(db)
    _crear_categorias_base(db)
    _crear_admin(db)
    _crear_peliculas(db)

def _crear_admin(db: Session):
    from app.models.cliente import Cliente
    from datetime import date
    existe = db.query(Cliente).filter(Cliente.cedula == ADMIN_DATA["cedula"]).first()
    if not existe:
        admin = Cliente(
            cedula=ADMIN_DATA["cedula"],
            nombre=ADMIN_DATA["nombre"],
            hashed_password=pwd_context.hash(ADMIN_DATA["password"]),
            is_admin=True,
            fecha_ingreso=date.today(),
        )
        db.add(admin)
        db.commit()

def _crear_clasificaciones_base(db: Session):
    from app.models.clasificacion import Clasificacion
    if db.query(Clasificacion).count() == 0:
        for nombre in ["Apto para todo público", "Mayores de 13", "Mayores de 18"]:
            db.add(Clasificacion(nombre=nombre))
        db.commit()

def _crear_categorias_base(db: Session):
    from app.models.categoria import Categoria
    nombres = ["Accion", "Ciencia Ficcion", "Drama", "Terror", "Comedia", "Tendencias"]
    for nombre in nombres:
        if not db.query(Categoria).filter(Categoria.nombre == nombre).first():
            db.add(Categoria(nombre=nombre))
    db.commit()

def _crear_peliculas(db: Session):
    from app.models.video import Video
    from app.models.categoria import Categoria
    for p in PELICULAS:
        if not db.query(Video).filter(Video.isan == p["isan"]).first():
            video = Video(
                isan=p["isan"],
                titulo_original=p["titulo_original"],
                anio_produccion=p["anio_produccion"],
                duracion=p["duracion"],
                tipo=p["tipo"],
                descripcion=p.get("descripcion", ""),
                imagen_url=p.get("imagen_url", ""),
                trailer_url=p.get("trailer_url", ""),
                clasificacion_id=p["clasificacion_id"],
                precio_renta=Decimal(str(p.get("precio_renta", "3.99"))),
            )
            db.add(video)
            db.flush()
            for cat_nombre in p.get("categorias", []):
                cat = db.query(Categoria).filter(Categoria.nombre == cat_nombre).first()
                if cat:
                    video.categorias.append(cat)
        db.commit()
