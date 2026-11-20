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