import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import db

origins = [
    o.strip()
    for o in os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
    ).split(",")
]

app = FastAPI(
    title = "ZimGENE API",
    description = "Read-only API for the Zimbabwe genomic curation prototype.",
    version = "0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Simple health check that confirms the API is running."""
    return {"message": "ZimGENE API is running."}


@app.get("/species")
def list_species(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):

    """Return species> Use ?limit= and ?offset= to page through."""
    conn = db.get_connection()
    try:
        return db.get_all_species(conn, limit, offset)
    finally:
        conn.close()


@app.get("/species/{species_id}")
def get_species(species_id: int):
    """Return one species by its species_id."""
    conn = db.get_connection()
    try:
        species = db.get_species_by_id(conn, species_id)
        if species is None:
            raise HTTPException(status_code=404, detail="Species not found")
        return species
    finally:
        conn.close()


@app.get("/pathogens")
def list_pathogens(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """Return pathogens. Use ?limit= and ?offset= to page through."""
    conn = db.get_connection()
    try:
        return db.get_all_pathogens(conn, limit, offset)
    finally:
        conn.close()


@app.get("/pathogens/{pathogen_id}")
def get_pathogen(pathogen_id: int):
    """Return one pathogen by its pathogen_id."""
    conn = db.get_connection()
    try:
        pathogen = db.get_pathogen_by_id(conn, pathogen_id)
        if pathogen is None:
            raise HTTPException(status_code=404, detail="Pathogen not found")
        return pathogen
    finally:
        conn.close()


@app.get("/organisms")
def list_organisms(host_status: str = None, species_name: str = None, pathogen_name: str = None, limit: int = Query(100, ge=1, le=500), offset: int = Query(0, ge=0)):
    """Return one page of organisms..."""
    conn = db.get_connection()
    try:
        return db.get_all_organisms(conn, host_status, species_name, pathogen_name, limit, offset)
    finally:
        conn.close()


@app.get("/organisms/{organism_id}")
def get_organism(organism_id: int):
    """Return one organism by its organism_id, with readable species and pathogen information."""
    conn = db.get_connection()
    try:
        organism = db.get_organism_by_id(conn, organism_id)
        if organism is None:
            raise HTTPException(status_code=404, detail="Organism not found")
        return organism
    finally:
        conn.close()


@app.get("/sequences")
def list_sequences(
    limit: int = Query(100, ge=1, le=500), 
    offset: int = Query(0, ge=0)
):
    """Return a lightweight summary of every sequence Use ?limit= and ?offset= to page through results."""
    conn = db.get_connection()
    try:
        return db.get_all_sequences(conn, limit, offset)
    finally:
        conn.close()


@app.get("/sequences/{sequence_id}")
def get_sequence(sequence_id: int):
    """Return full detail for one sequence, including the raw sequence and annotations."""
    conn = db.get_connection()
    try:
        sequence = db.get_sequence_by_id(conn, sequence_id)
        if sequence is None:
            raise HTTPException(status_code=404, detail="Sequence not found")
        return sequence
    finally:
        conn.close()



@app.get("/collection_site")
def list_collection_sites(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """Return collection sites. Use ?limit= and ?offset= to page through results."""
    conn = db.get_connection()
    try:
        return db.get_all_collection_sites(conn, limit, offset)
    finally:
        conn.close()


@app.get("/collection_site/{site_id}")
def get_collection_site(site_id: int):
    """Return one collection site by its site_id."""
    conn = db.get_connection()
    try:
        site = db.get_collection_site_by_id(conn, site_id)
        if site is None:
            raise HTTPException(status_code=404, detail="Collection site not found")
        return site
    finally:
        conn.close()


@app.get("/qc")
def list_qc_metrics(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """Return QC metrics. Use ?limit= and ?offset= to page through results."""
    conn = db.get_connection()
    try:
        return db.get_all_qc_metrics(conn, limit, offset)
    finally:
        conn.close()


@app.get("/qc/{qc_id}")
def get_qc_metric(qc_id: int):
    """Return one row from the qc table by qc_id."""
    conn = db.get_connection()
    try:
        qc_metric = db.get_qc_metrics_by_id(conn, qc_id)
        if qc_metric is None:
            raise HTTPException(status_code=404, detail="QC metric not found")
        return qc_metric
    finally:
        conn.close()