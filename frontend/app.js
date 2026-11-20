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