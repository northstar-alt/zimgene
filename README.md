# ZimGENE

Curated genomic database and analysis pipeline for livestock and crop pathogens affecting Zimbabwe (FMDV, ASFV, TMV, Maize streak virus). Independent student project.

**Live demo:** https://zimgene-web.onrender.com
**API docs:** https://zimgene.onrender.com/docs

![ZimGENE homepage showing organisms and sequences tables](docs/screenshot.png)

---

## What it does

1. A Python/BioPython pipeline pulls sequence records from NCBI via Entrez.
2.  Records are stored in a normalized PostgreSQL schema (9 tables).
3. R scripts produce GC-content and sequence-length visualizations.
4. A read-only FastAPI service exposes the data over HTTPS.
5. A plain HTML/CSS/JS frontend displays organisms and sequences.

---

## Tech Stack & Dependencies

PostgreSQL (Neon), Python (BioPython, psycopg 3, FastAPI), R (ggplot2),
HTML/CSS/JavaScript. Hosted on Render.

---

## API endpoints

| Endpoint | Description |
|---|---|
| /species, /species/{id} | Host species |
| /pathogens, /pathogens/{id} | Pathogens |
| /organisms | Specimens (filter: host_status, species_name, pathogen_name) |
| /sequences, /sequences/{id} | Sequence summaries and full records |
| /collection_site, /qc | Collection sites and QC records |

All list endpoints support ?limit= and ?offset=.

---

## Getting started

Developed and tested with PostgreSQL 18 and Python 3.14. R and RStudio are optional (for the plots).

### 1. Database
Create a database, then load the schema:

```
psql -U postgres -d prototype -f sql/zimgene_schema.sql
```

### 2. Ingestion pipeline (`python/`)
Create `python/.env`:

```env
PG_HOST=localhost
PG_PORT=5432
PG_DBNAME=prototype
PG_USER=postgres
PG_PASSWORD=your_password_here
NCBI_EMAIL=your_email@example.com
NCBI_API_KEY=optional
```

Then: `pip install -r requirements.txt` and `python ingest.py`

### 3. API (`api/`)
Create `api/.env` with the same `PG_*` values (or a single `DATABASE_URL` for a hosted database), then:

```
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Set `CORS_ORIGINS` to your frontend's address if it differs from the localhost defaults.

### 4. Frontend (`frontend/`)
Set `API_URL` at the top of `app.js`, then run `python -m http.server 5500` from that folder.

 ---

 ## Data and limitations
- Sequence data comes from NCBI GenBank. Search results are filtered
  to exclude PDB and patent records, but records are not independently verified.
- QC records mark NCBI accessions as pre-validated; no independent
  coverage analysis is performed at this stage.
- The free hosting tier sleeps when idle, so the first request can take up to a minute.

---

## Database Architecture Highlights

The PostgreSQL schema (`zngd_schema.sql`) uses a normalized structure:

1. **`species` & `pathogen`**: Reference tables for hosts (livestock/plants) and infectious pathogens.
2. **`collection_site`**: Geographic locations tracking district, province, and coordinates.
3. **`organism`**: Specimen records linking host, pathogen, collection site, and contributor.
4. **`sequence`**: Genomic sequence records containing raw FASTA sequences, length, GC percentage, and `JSONB` feature annotations.
5. **`audit_log`**: Generic change-tracking table capturing `insert`, `update`, and `delete` events as JSON objects.

---

## Disclaimer
Independent student project, not affiliated with any government body.

---
