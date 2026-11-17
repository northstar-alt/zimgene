import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Connect using DATABASE_URL if set, otherwise the local PG_* settings."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg.connect(
            database_url,
            row_factory=dict_row,
        )
    return psycopg.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=os.getenv("PG_PORT", "5432"),
        dbname=os.getenv("PG_DBNAME", "prototype"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD", ""),
        row_factory=dict_row,
    )

def get_all_species(conn, limit=100, offset=0):
    """Return species, one page at a time."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM species ORDER BY species_id LIMIT %s OFFSET %s;", (limit, offset))
        return cur.fetchall()

def get_species_by_id(conn, species_id):
    """Return a single row from the species table by species_id (one row or None if it doesn't exist)."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM species WHERE species_id = %s;",
              (species_id,),
              )
        return cur.fetchone()

def get_all_pathogens(conn, limit=100, offset=0):
    """Return pathogens, one page at a time."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM pathogen ORDER BY pathogen_id LIMIT %s OFFSET %s;", (limit, offset))
        return cur.fetchall()

def get_pathogen_by_id(conn, pathogen_id):
    """Return a single row from the pathogens table by pathogen_id (one row or None if it doesn't exist)."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM pathogen WHERE pathogen_id = %s;",
              (pathogen_id,),
              )
        return cur.fetchone()

def get_all_organisms(conn, host_status=None, species_name=None, pathogen_name=None, limit=100, offset=0):
    """Return one page of organisms..."""
    query = """
        SELECT 
            o.organism_id,
            s.scientific_name AS species_name,
            p.scientific_name AS pathogen_name,
            o.collection_date,
            o.specimen_type,
            o.host_status,
            o.notes
        FROM organism o
        JOIN species s ON o.species_id = s.species_id
        LEFT JOIN pathogen p ON o.pathogen_id = p.pathogen_id
        WHERE 1=1
    """
    params = []

    if host_status:
        query += " AND o.host_status = %s"
        params.append(host_status)

    if species_name:
        query += " AND s.scientific_name = %s"
        params.append(species_name)

    if pathogen_name:
        query += " AND p.scientific_name = %s"
        params.append(pathogen_name)

    query += " ORDER BY o.organism_id LIMIT %s OFFSET %s;"

    with conn.cursor() as cur:
        cur.execute(query, params + [limit, offset])
        return cur.fetchall()


def get_organism_by_id(conn, organism_id):
    """Return a single organism ID, joined with its species and pathogen information"""
    query = """
        SELECT 
            o.organism_id,
            s.scientific_name AS species_name,
            p.scientific_name AS pathogen_name,
            o.collection_date,
            o.specimen_type,
            o.host_status,
            o.notes
        FROM organism o
        JOIN species s ON o.species_id = s.species_id
        LEFT JOIN pathogen p ON o.pathogen_id = p.pathogen_id
        WHERE o.organism_id = %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (organism_id,))
        return cur.fetchone()


def get_all_sequences(conn, limit=100, offset=0):
    """Return a light summary of every sequence, one page at a time."""
    query = """
                SELECT 
                    sequence_id,
                    organism_id,
                    ncbi_accession,
                    sequence_type,
                    sequence_length,
                    gc_content,
                    retrieved_at
                FROM sequence
                ORDER BY sequence_id
                LIMIT %s OFFSET %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (limit, offset))
        return cur.fetchall()

def get_sequence_by_id(conn, sequence_id):
    """Return full detail for a single sequence plus a raw sequence and the annotations."""
    query = """
        SELECT *
        FROM sequence
        WHERE sequence_id = %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (sequence_id,))
        return cur.fetchone()


def get_all_collection_sites(conn, limit=100, offset=0):
    """Return every site, one page at a time."""
    query = """
        SELECT 
        site_id,
        site_name,
        province,
        district,
        latitude,
        longitude,
        site_type
        FROM collection_site
        ORDER BY site_id;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_collection_site_by_id(conn, site_id):
    """Return a single row from the collection_site table by site_id (one row or None if it doesn't exist)."""
    query = """
        SELECT *
        FROM collection_site
        WHERE site_id = %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (site_id,))
        return cur.fetchone()


def get_all_qc_metrics(conn, limit=100, offset=0):
    """Return every row in the qc table in the database."""
    query = """
        SELECT *
        FROM qc
        ORDER BY qc_id
        LIMIT %s OFFSET %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (limit, offset))
        return cur.fetchall()


def get_qc_metrics_by_id(conn, qc_id):
    """Return a single row from the qc table by qc_id (one row or None if it doesn't exist)."""
    query = """
        SELECT *
        FROM qc
        WHERE qc_id = %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (qc_id,))
        return cur.fetchone()
