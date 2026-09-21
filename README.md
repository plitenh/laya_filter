# Laya — filtre d’intégration d’actualités

Décisions [Laya](https://github.com/NandhaKishorM/laya) sur deux axes : **faits** et **préférences**.
L’annotation corrige la justesse champ par champ ; le **diff** montre `avant → après`.

Dépôt : https://github.com/plitenh/laya_filter

> Langue du dépôt : **français**.  
> Interface locale (guides, CLI, rapports) : **chinois + anglais** (`zh` / `en`).

## Axes

| Axe | Champs | Rôle |
|-----|--------|------|
| Fait | `factual` / `claim_status` | Solidité et statut de l’affirmation |
| Préférence | `channel` / `publish` / `salience` | Rubrique, publication, saillance |

## Diff d’annotation

```
article + prédiction Laya
        │
        ▼
  marques  keep | fix | flag
        │
        ▼
  diff de champs
        ├─ diffs.md / diffs.unified.txt
        └─ annotated_gold.jsonl
```

- `keep` — champ correct  
- `fix` — remplacer par `after`  
- `flag` — doute, hors or

## Démarrage

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# échantillon unique dans le dépôt ; générer plus en local
python agent/m1/generate_news.py --n 8 --out agent/data/sample.jsonl

# pupitre d’annotation (sorties locales zh/en)
python agent/annotate/desk.py build --corpus agent/data/sample.jsonl --limit 8
python agent/annotate/desk.py demo
```

Exemple de feuille :

```json
{
  "id": "news-0001",
  "marks": {"factual": "fix", "channel": "keep"},
  "after": {"factual": false},
  "notes": {"factual": "headline overstates the body"}
}
```

## Arborescence

| Chemin | Contenu |
|--------|---------|
| `agent/m1/schema.py` | Schéma principal (axes) |
| `agent/data/sample.jsonl` | Seul échantillon versionné (8 lignes) |
| `agent/annotate/diff.py` | Diff de champs |
| `agent/annotate/desk.py` | Pupitre |
| `agent/i18n.py` | Chaînes locales zh / en |

Les poids du modèle ne sont pas versionnés. Variables : `LAYA_FILTER_ROOT`, `LAYA_MODELS`, `LAYA_LANG=zh|en`.
