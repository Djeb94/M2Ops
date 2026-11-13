## Architecture

```mermaid
flowchart TB
    SRC["Flux RSS · 8 sources<br/>titre, extrait, lien, date"]

    subgraph RUN["Docker Compose · nos postes, puis serveur fourni"]
        C["1 · Collecte<br/>Python + feedparser"]
        B[("2 · Stockage brut<br/>PostgreSQL, tel quel")]
        N["3 · Nettoyage, qualité<br/>règles + rapport"]
        P[("Stockage propre<br/>PostgreSQL, moins de 24 h")]
        T["4 · Thèmes<br/>TF-IDF + clustering"]
        L["5 · Livraison<br/>édition statique, 7 h"]
        ORCH{{"Orchestrateur<br/>planifie, relance (choix TD 3)"}}
        S["6 · Supervision<br/>Prometheus + Grafana"]
    end

    PUB(["Lecteurs<br/>l'édition du jour"])

    SRC --> C --> B --> N --> P --> T --> L --> PUB
    ORCH -.-> C & N & T & L
    C & N & T & L -.-> S

    classDef traitement fill:#EEEDFE,stroke:#534AB7,color:#26215C
    classDef stockage fill:#E1F5EE,stroke:#0F6E56,color:#04342C
    classDef exploitation fill:#FAECE7,stroke:#993C1D,color:#4A1B0C
    classDef externe fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    class C,N,T,L traitement
    class B,P stockage
    class ORCH,S exploitation
    class SRC,PUB externe
    linkStyle 7,8,9,10 stroke:#D85A30,stroke-dasharray:5 4
    linkStyle 11,12,13,14 stroke:#888780,stroke-dasharray:2 3
```

**Légende** : violet = traitement · vert = stockage · orange = exploitation ·
pointillés orange = l'orchestrateur déclenche · pointillés gris = métriques et journaux vers la supervision.