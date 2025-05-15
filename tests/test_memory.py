from mnemonic.mnemonic_memory import MnemonicMemory

def test_memory_add_and_search():
    memory = MnemonicMemory(backend="json")  # ou "faiss" si FAISS est bien configuré

    memory.add(
        input="Pourquoi la mer est salée ?",
        output="À cause des sels minéraux issus de l'érosion.",
        tags=["science"],
        source="inconnu"
    )

    results = memory.search("Pourquoi la mer est salée ?", top_k=1)
    
    assert len(results) >= 1
    assert "output" in results[0]
    assert "mer" in results[0]["input"]

def test_memory_delete():
    memory = MnemonicMemory(backend="json")

    memory_id = memory.add(
        input="Que reste-t-il du vent passé ?",
        output="Quelques feuilles mortes.",
        tags=["poésie"]
    )

    added = memory.get(memory_id)
    assert added is not None
    assert "vent" in added["input"]

    deleted = memory.delete(memory_id)
    assert deleted is True

    assert memory.get(memory_id) is None
