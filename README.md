# Mnemonic – Mémoire vectorielle locale pour IA

[![Tests](https://github.com/Ybucaille/Mnemonic/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/Ybucaille/Mnemonic/actions/workflows/tests.yml)
[![version](https://img.shields.io/github/v/tag/Ybucaille/Mnemonic?label=version)](https://github.com/Ybucaille/Mnemonic/releases/latest)
[![License](https://img.shields.io/github/license/Ybucaille/Mnemonic?cacheSeconds=60)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)](https://github.com/Ybucaille)

Mnemonic est un moteur de mémoire vectorielle local et autonome, conçu pour stocker et retrouver des souvenirs riches de sens : prompts, réponses, réflexions, faits.
Il s’intègre facilement à tout agent (comme [Nexus](https://github.com/Ybucaille/Nexus)) et fournit une continuité contextuelle à vos systèmes.

## Fonctionnalités

- Ajout de souvenirs : texte, tags, timestamp, source, métadonnées
- Recherche vectorielle : par similarité sémantique (cosine ou FAISS)
- Filtrage avancé : par tags, date (avant/après)
- Persistance locale : en `.jsonl` (léger) ou via `FAISS` (scalable)
- Interface unifiée : `MnemonicMemory` choisit automatiquement le backend
- Fonctionne entièrement hors ligne

## Structure du projet

```
Mnemonic/
├── mnemonic/                  # Code source principal
│   ├── __init__.py            # Expose MnemonicMemory
│   ├── memory_interface.py    # Interface abstraite
│   ├── memory_store.py        # Backend JSONL
│   ├── faiss_memory_store.py  # Backend FAISS
│   ├── embedding_model.py     # Modèle de vectorisation
│   ├── mnemonic_memory.py     # Classe centrale unifiée
│   └── utils.py               # Filtres (tags, dates)
│
├── data/                      # Fichiers persistants
│   ├── memory.jsonl           # Souvenirs
│   └── index.faiss            # Index vectoriel
│
├── examples/                  # Démonstrations et API
│   ├── demo.py
│   ├── api.py
│   └── client.py
│
├── tests/                     # Tests unitaires
│   └── test_memory.py
│
├── README.md
├── requirements.txt
```

## Exemple d’utilisation

```python
from mnemonic import MnemonicMemory

memory = MnemonicMemory(backend="auto")

memory.add(
    input="Pourquoi le ciel est bleu ?",
    output="À cause de la diffusion de Rayleigh.",
    tags=["physique"],
    source="wiki"
)

résultats = memory.search(
    query="Pourquoi voit-on du bleu dans le ciel ?",
    tags=["physique"],
    after="2025-01-01"
)

for r in résultats:
    print(f"{r['timestamp']} → {r['output']}")
```

```
2025-05-15T19:11:54.635058 → À cause de la diffusion de Rayleigh.
```


## Lancer l’API REST (optionnel)

Mnemonic peut être lancé en tant qu’API HTTP locale avec FastAPI.

### 1. Lancer le serveur

```
uvicorn examples.api:app --reload
```

Le serveur est disponible sur `http://localhost:8000`

### 2. Endpoints disponibles

- `POST /memory/add`  
  Ajouter un souvenir (input/output/tags/source)

- `GET /memory/search`  
  Rechercher un souvenir via une requête vectorielle  
  Exemple :  
  ```
  /memory/search?query=le+ciel+est+bleu&tags=physique&after=2025-01-01
  ```

- `GET /memory/all`  
  Voir tous les souvenirs, avec filtres (tags/date)

- `DELETE /memory/delete?id=...`  
  Supprimer un souvenir via son identifiant

### 3. Tester avec un client Python

Un script de test est disponible dans `examples/client.py` :

```
python examples/client.py
```

## Cas d’usage

- Agent conversationnel : garde mémoire des échanges
- Recherche augmentée locale : stocke des extraits/documentations vectorisés
- Mémoire d’auteur : enregistre idées, réflexions, brouillons
- IA réflexive : trace de raisonnement, analyse cognitive

## Installation

```
git clone https://github.com/Ybucaille/Mnemonic.git
cd Mnemonic
pip install -r requirements.txt
```

Requiert Python 3.9+, sentence-transformers, faiss-cpu.

## Version actuelle

| Version | Fonctionnalité                     | Statut     |
|---------|-------------------------------------|------------|
| v1.0    | Mémoire vectorielle locale (JSON/FAISS) | Stable     |
| v1.1    | Interface REST                      | Stable |
| v1.2    | Résumés auto / oubli progressif     | Non prévu  |
| v2.0    | Mémoire multi-agent                 | En réflexion |

## Licence

MIT — libre à utiliser, modifier, intégrer.
