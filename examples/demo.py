from core import MnemonicMemory

memory = MnemonicMemory(backend="auto")

memory.add(
    input="Pourquoi le ciel est bleu ?",
    output="À cause de la diffusion de Rayleigh.",
    tags=["physique"],
    source="wiki"
)

# Recherche filtrée
résultats = memory.search(
    query="Pourquoi le ciel est bleuté",
    tags=["physique"],
    after="2025-01-01"
)

for r in résultats:
    print(f"{r['timestamp']} → {r['output']}")