const API_URL = "https://zimgene.onrender.com";

async function loadSpecies() {
    const list = document.getElementById("species-list");
    list.textContent = "Loading...";
    try {
        const response = await fetch(`${API_URL}/species`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        const species = await response.json();
        list.textContent = "";
        for  (const s of species) {
            const item = document.createElement("li");
             item.textContent = `${s.common_name} (${s.scientific_name}) - ${s.category}`;
            list.appendChild(item);
        }
    } catch (error) {
        list.textContent = "Could not load species. The server may be waking up, try again in a minute.";
        console.error(error);
    }
}

loadSpecies();

async function loadOrganisms() {
    const status = document.getElementById("status-filter").value;
    const query = status ? `?host_status=${status}` : "";
    const body = document.querySelector("#organism-table tbody");
    body.textContent = "";
    try {
        const response = await fetch(`${API_URL}/organisms${query}`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        const organisms = await response.json();
        for (const o of organisms) {
            const row = document.createElement("tr");
            const cells = [
                o.species_name,
                o.pathogen_name ?? "None (healthy)",
                o.host_status,
                o.collection_date,
            ];
            for (const text of cells) {
                const cell = document.createElement("td");
                cell.textContent = text;
                row.appendChild(cell);  
            }
            body.appendChild(row);
        }
    } catch (error) {
        console.error(error);
    }
}

document.getElementById("status-filter").addEventListener("change", loadOrganisms);
loadOrganisms();

const PAGE_SIZE = 10;
let sequenceOffset = 0;

async function loadSequences() {
    const body = document.querySelector("#sequence-table tbody");
    body.textContent = "";
    try {
        const response = await fetch(
            `${API_URL}/sequences?limit=${PAGE_SIZE + 1}&offset=${sequenceOffset}`
        );
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        const rows = await response.json();
        const hasNext = rows.length > PAGE_SIZE;
        const page = rows .slice(0, PAGE_SIZE);

        for (const s of page) {
            const row = document.createElement("tr");

           const accessionCell = document.createElement("td");
           const link = document.createElement("a");
           link.href = `https://www.ncbi.nlm.nih.gov/nuccore/${encodeURIComponent(s.ncbi_accession)}`;
           link.textContent = s.ncbi_accession;
           link.target = "_blank";
           link.rel = "noopener";
           accessionCell.appendChild(link);
           row.appendChild(accessionCell);

           for (const text of [s.sequence_type, s.sequence_length, s.gc_content]) {
                const cell = document.createElement("td");
                cell.textContent = text;
                row.appendChild(cell);
            }
            body.appendChild(row);
        }

        document.getElementById("page-label").textContent = 
            ` Page ${sequenceOffset / PAGE_SIZE + 1} `;
        document.getElementById("prev-page").disabled = sequenceOffset === 0;
        document.getElementById("next-page").disabled = !hasNext;
    } catch (error) {
        console.error(error);
    }
}

document.getElementById("prev-page").addEventListener("click", () => {
    sequenceOffset -= PAGE_SIZE;
    loadSequences();
});

document.getElementById("next-page").addEventListener("click", () => {
    sequenceOffset += PAGE_SIZE;
    loadSequences();
});

loadSequences();
