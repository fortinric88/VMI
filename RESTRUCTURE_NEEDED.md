# ⚠️ IMPORTANT: Restructuration requise pour Home Assistant

Home Assistant a besoin d'une structure précise. Voici ce qui est attendu :

## Structure attendue par Home Assistant

```
Repository Root/
├── manifest.json        ← DOIT être à la racine
├── Dockerfile           ← DOIT être à la racine  
├── requirements.txt
├── run.sh
├── README.md
└── ...autres fichiers
```

## Structure actuelle (❌ Ne fonctionne pas)

```
Repository Root/
├── HA_VMI/
│   ├── manifest.json   ← ❌ Trop profond
│   ├── Dockerfile      ← ❌ Trop profond
│   └── ...
└── repository.json
```

## Solutions

### ✅ Solution 1: Créer un dépôt séparé pour l'addon
Recommandé pour une meilleure organisation.

```bash
# 1. Créer un nouveau dépôt GitHub: ha-vmi
# 2. Copier le contenu de HA_VMI/ à la racine
# 3. Ajouter le dépôt à Home Assistant:
#    https://github.com/fortinric88/ha-vmi
```

### ✅ Solution 2: Restructurer le dépôt actuel
Plus simple si vous voulez tout en un.

```bash
# 1. Déplacer les fichiers HA_VMI vers la racine:
mv HA_VMI/* .

# 2. Supprimer le dossier HA_VMI
rmdir HA_VMI

# 3. Mettre à jour repository.json
# 4. Commit et push
```

## Recommandation

**Solution 1** est meilleure car :
- Chaque addon a son propre dépôt
- Structure plus claire
- Facilite la maintenance et les mises à jour

À vous de choisir !
