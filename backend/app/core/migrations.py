"""Migraciones ligeras para SQLite (columnas nuevas sin recrear tablas)."""
from sqlalchemy import text
from sqlalchemy.engine import Engine


def run_migrations(engine: Engine) -> None:
    if "sqlite" not in str(engine.url):
        return
    with engine.connect() as conn:
        cols = {
            row[1]
            for row in conn.execute(text("PRAGMA table_info(videos)")).fetchall()
        }
        if "precio_renta" not in cols:
            conn.execute(
                text("ALTER TABLE videos ADD COLUMN precio_renta NUMERIC(10,2) DEFAULT 3.99")
            )
            conn.commit()

        hist_cols = {
            row[1]
            for row in conn.execute(text("PRAGMA table_info(historial)")).fetchall()
        }
        if hist_cols and "progreso" not in hist_cols:
            conn.execute(
                text("ALTER TABLE historial ADD COLUMN progreso INTEGER DEFAULT 0")
            )
            conn.commit()
