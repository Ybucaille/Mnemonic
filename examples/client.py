import requests

BASE_URL = "http://localhost:8000"

# Ajout d'un souvenir
add_payload = {
    "input": "Pourquoi le ciel est bleu ?",
    "output": "À cause de la diffusion de Rayleigh.",
    "tags": ["physique", "science"],
    "source": "curiosité",
    "metadata": {"importance": "moyenne"}
}

r_add = requests.post(f"{BASE_URL}/memory/add", json=add_payload)
print("Ajout :", r_add.json())

# Recherche d'un souvenir
params = {
    "query": "Pourquoi le ciel est bleu ?",
    "tags": "physique",
    "after": "2025-01-01"
}

r_search = requests.get(f"{BASE_URL}/memory/search", params=params)
print("Résultats de recherche :")
for mem in r_search.json():
    print(f"- {mem['timestamp']} → {mem['output']} (id: {mem['id']})")