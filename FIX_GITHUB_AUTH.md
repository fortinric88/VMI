# 🔧 Troubleshooting - Erreur 403 et remote déjà existant

## Problème 1: Remote origin already exists

```bash
# Supprimer le remote existant
git remote remove origin

# Ou voir les remotes existants
git remote -v
```

## Problème 2: Error 403 - Permission denied

Cela signifie que GitHub n'a pas pu vous authentifier. Voici les solutions :

### Solution A: Utiliser un Personal Access Token (recommandé)

```bash
# 1. Créer un token sur GitHub
# https://github.com/settings/tokens
# Scopes nécessaires: repo, workflow

# 2. Configurer git pour utiliser le token
git remote set-url origin https://<TOKEN>@github.com/fortinric88/ha-vmi.git

# Remplacez <TOKEN> par votre token réel
```

### Solution B: Utiliser SSH

```bash
# 1. Vérifier les clés SSH
cat ~/.ssh/id_rsa.pub

# 2. Si absent, créer une clé
ssh-keygen -t ed25519 -C "fortinric88@github.com"

# 3. Ajouter la clé à GitHub
# https://github.com/settings/keys

# 4. Configurer le remote en SSH
git remote remove origin
git remote add origin git@github.com:fortinric88/ha-vmi.git
```

### Solution C: Utiliser GitHub CLI (plus simple)

```bash
# 1. Installer gh CLI
sudo apt install gh

# 2. Authentifier
gh auth login

# 3. Push avec gh
gh repo create ha-vmi --source=. --remote=origin --push
```

## ✅ Étapes à suivre

### Si vous avez déjà créé le dépôt sur GitHub:

```bash
# 1. Nettoyer les remotes
git remote remove origin

# 2. Utiliser GitHub CLI (plus simple)
gh auth login
gh repo sync

# OU configurer le token
export GH_TOKEN="votre_token_ici"
git remote add origin https://$GH_TOKEN@github.com/fortinric88/ha-vmi.git
git push -u origin main
```

### Si vous n'avez PAS encore créé le dépôt:

```bash
# 1. Créer le dépôt avec gh CLI
gh repo create ha-vmi --public --source=. --remote=origin --push
```

## 📝 Créer un Personal Access Token

1. Allez sur https://github.com/settings/tokens/new
2. **Token name**: "ha-vmi-publish"
3. **Expiration**: 90 days
4. **Scopes**:
   - ☑️ repo (full control)
   - ☑️ workflow
5. Cliquez **Generate token**
6. **Copiez le token** (vous ne pourrez plus le voir après!)

## 🔐 Configurer le token dans git

```bash
# Configurer git avec le token
git remote set-url origin https://fortinric88:<TOKEN>@github.com/fortinric88/ha-vmi.git

# Tester la connection
git push -u origin main
```

## 🆘 Si ça ne fonctionne toujours pas

```bash
# 1. Vérifier votre authentification GitHub
gh auth status

# 2. Si non authentifié, se connecter
gh auth login

# 3. Utiliser gh pour pousser
gh repo create ha-vmi --public --source=. --push
```
