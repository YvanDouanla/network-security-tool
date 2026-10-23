# Network Security Tool

Projet pédagogique **DevSecOps** réalisé par **Douanla Yvan**, dans le cadre des TP ISRC5 / Institut F2I.

Le projet évolue d'un script Python de vérification de ports locaux vers une application conteneurisée avec **FastAPI**, **NGINX** et **Docker Compose**. Les changements sont suivis avec **Git et GitHub**, testés avec **pytest**, analysés avec **Bandit**, puis audités au niveau de l'image Docker avec **Trivy**. Les contrôles sont automatisés dans **GitHub Actions**.

> **Périmètre des essais :** le programme en ligne de commande et l'API ciblent `127.0.0.1`. Dans un conteneur, cette adresse désigne le conteneur lui-même, pas le PC Windows. Ce projet est un laboratoire pédagogique et n'est pas présenté comme un service de production prêt à déployer.

## Sommaire

- [État du dépôt et branches](#état-du-dépôt-et-branches)
- [Travaux réalisés](#travaux-réalisés)
- [Prérequis](#prérequis)
- [Installation locale et script Python](#installation-locale-et-script-python)
- [Tests, Bandit et bonus de compilation](#tests-bandit-et-bonus-de-compilation)
- [Application Docker : API et NGINX](#application-docker--api-et-nginx)
- [Durcissement des conteneurs](#durcissement-des-conteneurs)
- [Audit Trivy et comparaison avantaprès](#audit-trivy-et-comparaison-avantaprès)
- [Pipelines GitHub Actions](#pipelines-github-actions)
- [Organisation des fichiers](#organisation-des-fichiers)
- [Réponses, preuves et Pull Requests](#réponses-preuves-et-pull-requests)
- [Incidents rencontrés et corrections](#incidents-rencontrés-et-corrections)
- [Limites et pistes damélioration](#limites-et-pistes-damélioration)

## État du dépôt et branches

La documentation décrit l'ensemble du parcours, y compris le TP 3 encore développé sur sa branche dédiée.

| Branche | Contenu / rôle |
|---|---|
| `main` | Script refactorisé, tests pytest, analyse Bandit, workflow Python, bonus `compileall` et pièces des TP 1 et 2. |
| `feature/custom-port` | Historique de l'ajout de la saisie du port au TP 1. |
| `feature/ci-pipeline` | Historique du pipeline de tests et de sécurité du TP 2. |
| `feature/compile-check` | Historique du bonus de compilation Python. |
| `feature/docker-security` | API FastAPI, NGINX, Compose, durcissement, rapports Trivy, workflow de scan d'image et réponses du TP 3. |

**Pour suivre les commandes Docker de ce README, utiliser `feature/docker-security`.** Les fichiers du TP 3 ne sont pas encore intégrés à `main` à l'état documenté. La [PR n° 4](https://github.com/YvanDouanla/network-security-tool/pull/4) présente ces travaux, avec un contrôle Trivy en échec sur les vulnérabilités résiduelles.

Les branches historiques sont des références de travail ; elles ne sont nécessaires ni au lancement du script sur `main`, ni à l'utilisation de l'application sur la branche Docker.

## Travaux réalisés

### TP 1 — Git et GitHub

- Initialisation du dépôt local et création du `README.md`.
- Configuration de l'identité Git et premiers commits.
- Création de `network_check.py` : connexion TCP locale avec délai maximal.
- Remplacement du port fixe `80` par une saisie utilisateur sur `feature/custom-port`.
- Publication de `main` et de la branche de fonctionnalité.
- Relecture des modifications et fusion par Pull Request.
- Réponses aux quatre questions dans `REPONSES.md`.

Les ports demandés par le support pour les essais étaient `80`, `443` et `8080`. Un port fermé constitue un résultat réseau possible, pas une erreur Python.

### TP 2 — Tests automatisés et sécurité du code

- Refactorisation du script en fonctions importables : `is_valid_port` et `check_port`.
- Ajout du bloc `if __name__ == "__main__"` pour éviter une saisie interactive à l'import.
- Écriture et exécution de **trois tests pytest**.
- Analyse statique de `network_check.py` avec **Bandit**.
- Automatisation des contrôles avec GitHub Actions sur `push` et `pull_request`.
- Démonstration d'un échec volontaire : attente incorrecte `is False` pour le port `443`.
- Observation de `1 failed, 2 passed`, puis correction et retour au vert.
- Réponses aux cinq questions dans `REPONSES_TP2.md`.

**Bonus :** ajout de `python -m compileall -q network_check.py` au workflow. Cette commande vérifie la compilation syntaxique en bytecode. Elle n'exécute pas la logique applicative et ne remplace ni les tests pytest ni l'analyse Bandit.

### TP 3 — Docker, durcissement et Trivy

Le sujet supposait l'existence d'un projet NetSecure. Celui-ci n'étant pas disponible, le TP a été **adapté à `network-security-tool`**, en réutilisant le script existant. Une API FastAPI a été ajoutée, sans créer de projet Flask.

- Construction d'une première image API et démarrage avec NGINX via Compose.
- Reconnaissance des réseaux, ports, volumes et utilisateur du conteneur.
- Scan initial de l'image avec Trivy et conservation des résultats.
- Durcissement de l'image et de son exécution.
- Tests fonctionnels après modification et comparaison des scans.
- Intégration d'un scan d'image bloquant dans GitHub Actions.
- Analyse des vulnérabilités résiduelles et réponses aux huit questions dans `REPONSES_TP3.md`.

Aucune base de données n'a été ajoutée : cette application n'a pas besoin de persistance.

## Prérequis

| Usage | Prérequis |
|---|---|
| Gestion du projet | Git et accès au dépôt GitHub |
| Script, pytest et Bandit | Python **3.12** recommandé pour reproduire l'environnement du TP |
| Application conteneurisée | Docker et Docker Compose opérationnels ; conteneurs Linux |
| Windows | PowerShell ; Docker Desktop avec son moteur Linux démarré |
| Scans locaux | Trivy exécuté via `aquasec/trivy:0.76.1` ; aucune installation Trivy Windows nécessaire |

Une connexion Internet est nécessaire pour télécharger les dépendances, les images et la base de vulnérabilités Trivy.

Les commandes ci-dessous sont destinées à **PowerShell**, depuis la racine du dépôt, sauf indication contraire.

## Installation locale et script Python

### Récupérer le dépôt

```powershell
git clone https://github.com/YvanDouanla/network-security-tool.git
Set-Location network-security-tool
git switch main
```

Si le dépôt existe déjà, ouvrir son dossier et vérifier les modifications locales avec `git status` avant de changer de branche ou de récupérer des changements.

### Préparer l'environnement Python

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Si Python 3.12 est absent, l'installer d'abord. Avec le gestionnaire Python présent sur le poste de la séance, la commande était `py install 3.12`.

L'appel direct à l'interpréteur `.venv` évite de sélectionner par erreur une autre version Python et ne nécessite pas l'activation d'un script PowerShell.

### Lancer le vérificateur de port

```powershell
.\.venv\Scripts\python.exe network_check.py
```

Saisir un port entier, par exemple `443`.

| Résultat | Interprétation |
|---|---|
| `Open` | La connexion TCP à `127.0.0.1` a abouti. |
| `Closed` | La connexion n'a pas abouti ; cela ne distingue pas tous les cas de fermeture, filtrage ou indisponibilité. |

Dans sa version actuelle, la saisie CLI non numérique ou un port hors limites peut lever une exception. La validation de l'API est distincte et décrite plus bas.

### Fonctions disponibles

| Fonction | Rôle |
|---|---|
| `is_valid_port(port)` | Vérifie le type entier et l'intervalle `1` à `65535`. |
| `check_port(host, port, timeout=2)` | Valide le port puis tente une connexion TCP IPv4 ; renvoie un booléen. |

La fonction générique accepte un argument `host`, mais les interfaces livrées du TP fixent leur cible à `127.0.0.1`.

## Tests, Bandit et bonus de compilation

```powershell
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m bandit -r network_check.py
.\.venv\Scripts\python.exe -m compileall -q network_check.py
```

| Contrôle | Résultat observé pendant le TP |
|---|---|
| pytest | **3 passed** après correction de l'échec volontaire |
| Bandit | **No issues identified** sur le fichier analysé |
| Compilation | Étape ajoutée au workflow du bonus |

Les tests vérifient un port valide, le rejet des valeurs `0` et `70000`, et la levée d'une `ValueError` par `check_port` pour un port invalide.

**Ils ne dépendent pas d'un service réellement ouvert sur 443** : la validation numérique n'ouvre aucune socket. L'appel à `check_port` utilise un port invalide, rejeté avant la création de la socket. Ces tests ne couvrent donc pas entièrement la connexion réseau.

Un résultat Bandit sans signalement ne garantit pas l'absence de toute faille ; il décrit le résultat des règles exécutées sur le périmètre analysé.

## Application Docker : API et NGINX

### Utiliser la branche du TP 3

```powershell
git fetch origin
git switch feature/docker-security
docker info
docker compose version
```

Sur un clone neuf, `git switch` peut créer la branche locale à partir de sa branche distante de même nom. Vérifier `git status` avant de changer de branche si des fichiers ont été modifiés.

### Construire et démarrer

```powershell
docker compose config --quiet
docker compose up -d --build
docker compose ps
```

Le contexte de construction est la **racine du dépôt**. Le Dockerfile se trouve dans `api/`, mais doit aussi copier `network_check.py`, situé à la racine.

Pour construire uniquement l'image API durcie avec vérification de la base distante :

```powershell
docker compose build --pull --no-cache api
```

### Architecture durcie

| Service | Rôle | Réseaux | Port publié sur Windows |
|---|---|---|---|
| `nginx` | Point d'entrée HTTP et reverse proxy vers `api:8000` | `frontend`, `backend` | `127.0.0.1:8080` vers le port conteneur `80` |
| `api` | FastAPI / Uvicorn et réutilisation de `check_port` | `backend` | Aucun |

Le réseau `backend` est déclaré `internal: true`. NGINX et l'API partagent ce réseau pour leurs communications légitimes. Seul NGINX dispose d'un port hôte publié dans la configuration durcie.

Le fichier `nginx/default.conf` est monté dans `/etc/nginx/conf.d/default.conf` en lecture seule. `create_host_path: false` empêche la création silencieuse d'un dossier si la source de montage n'existe pas.

### Routes et essais

| Route via NGINX | Description |
|---|---|
| `http://localhost:8080/` | Identité et état de l'application |
| `http://localhost:8080/health` | Disponibilité de l'API |
| `http://localhost:8080/check?port=8000` | Test TCP sur le port 8000 du conteneur API |
| `http://localhost:8080/docs` | Documentation interactive FastAPI |

```powershell
Invoke-RestMethod "http://localhost:8080/health"
Invoke-RestMethod "http://localhost:8080/check?port=8000"
docker compose exec api id
```

Résultats observés : `status: ok`, `open: True` pour le port 8000 et `uid=10001(appuser)`.

Le port 8000 est ouvert dans le conteneur API parce qu'Uvicorn y écoute. Cela **ne signifie pas que le port 8000 de Windows est ouvert**. La route `/check` impose une valeur de port entre `1` et `65535` ; les paramètres invalides sont rejetés par la validation FastAPI.

### Logs et arrêt

```powershell
docker compose logs --tail 50 api nginx
docker compose down
```

L'arrêt des conteneurs ne supprime pas les fichiers de rapports présents sur le poste.

## Durcissement des conteneurs

| Mesure appliquée à l'API | Objectif |
|---|---|
| `python:3.12` remplacée par `python:3.12-slim` | Réduire les composants et outils inutiles embarqués |
| `USER 10001:10001` | Éviter l'exécution du processus applicatif en root |
| Suppression du port API publié | Garder NGINX comme point d'entrée hôte |
| `backend` interne | Limiter la connectivité extérieure de l'API |
| `read_only: true` | Limiter les écritures dans le système de fichiers |
| `/tmp` en `tmpfs` | Autoriser les fichiers temporaires sans rendre toute l'image inscriptible |
| `cap_drop: [ALL]` | Retirer les capacités Linux inutiles à l'API |
| `no-new-privileges:true` | Empêcher l'acquisition de nouveaux privilèges par le processus |
| Copie explicite des fichiers / `.dockerignore` | Réduire le contexte de construction et éviter les archives d'audit dans le build |

`PYTHONDONTWRITEBYTECODE=1` évite l'écriture de bytecode dans le système de fichiers en lecture seule. `PYTHONUNBUFFERED=1` facilite la lecture immédiate des logs.

Ces restrictions d'exécution ne corrigent pas les CVE des bibliothèques. Elles réduisent les possibilités d'action après une compromission. NGINX reste basé sur son image standard ; il n'est pas présenté comme entièrement durci ou audité par le seul scan API.

## Audit Trivy et comparaison avant/après

### Résultats du laboratoire — 23 octobre 2026

| Indicateur | Image initiale `before` | Image durcie `after` |
|---|---:|---:|
| HIGH | 434 | **44** |
| CRITICAL | 24 | **0** |
| Total HIGH/CRITICAL | 458 | **44** |
| Espace disque affiché par Docker | 1,64 Go | **201 Mo** |
| Taille du contenu affichée par Docker | 421 Mo | **48,7 Mo** |
| Utilisateur API | root, UID 0 | **appuser, UID 10001** |

La réduction des occurrences HIGH/CRITICAL est d'environ **90,4 %**. La réduction de taille est d'environ **88 %** selon les mesures Docker observées.

Les occurrences sont comptées par paquet et vulnérabilité ; elles ne correspondent pas forcément à des CVE distinctes. Ces résultats décrivent les images et la base Trivy de la séance. Un nouveau scan peut donner des chiffres différents.

**Les 44 HIGH restantes n'avaient aucune version corrigée renseignée dans le rapport.** Elles restent des risques à suivre. Cela n'établit ni l'absence définitive de correctif, ni l'exploitabilité systématique de chaque faille.

Les résultats détaillés sont conservés dans le [dossier `audit` de la branche Docker](https://github.com/YvanDouanla/network-security-tool/tree/feature/docker-security/audit).

### Reproduire le scan de l'image durcie

Depuis `feature/docker-security`, après construction de l'image :

```powershell
docker pull aquasec/trivy:0.76.1
New-Item -ItemType Directory -Force audit | Out-Null
docker image save --output .\audit\api-after.tar network-security-tool-api:after
```

Scanner l'archive et conserver un rapport JSON :

```powershell
docker run --rm --mount "type=bind,source=$((Get-Location).Path)\audit,target=/audit" --mount "type=volume,source=trivy-cache,target=/root/.cache/trivy" aquasec/trivy:0.76.1 image --input /audit/api-after.tar --scanners vuln --severity HIGH,CRITICAL --format json --output /audit/trivy-after.json
$LASTEXITCODE
Test-Path .\audit\trivy-after.json
```

Ici, l'absence de `--exit-code 1` signifie qu'un code `0` indique la réussite technique du scan, même si des vulnérabilités sont détectées. Vérifier le code immédiatement après la commande, puis la présence et la validité du rapport.

Pour reproduire le **seuil bloquant de la CI**, afficher les résultats avec :

```powershell
docker run --rm --mount "type=bind,source=$((Get-Location).Path)\audit,target=/audit,readonly" --mount "type=volume,source=trivy-cache,target=/root/.cache/trivy" aquasec/trivy:0.76.1 image --input /audit/api-after.tar --scanners vuln --severity HIGH,CRITICAL --exit-code 1
```

### Interpréter le code de sortie

- Scan terminé avec code `0` sans seuil configuré : l'analyse a abouti, pas nécessairement sans CVE.
- Scan avec `--exit-code 1` et résultats HIGH/CRITICAL : échec attendu du contrôle de sécurité.
- Erreur de téléchargement, d'archive ou de lecture : incident technique à diagnostiquer ; ne pas le présenter comme un résultat de vulnérabilités.
- Rapport absent : résultat **indisponible**, et non « zéro vulnérabilité ».

Les archives `audit/*.tar` sont exclues de Git. Les fichiers JSON, TXT et CSV peuvent être conservés comme preuves. `audit/Dockerfile.before` et `audit/compose.before.yaml` décrivent l'état initial ; les fichiers actifs sont `api/Dockerfile` et `compose.yaml`.

Pour reconstruire séparément la variante initiale à des fins de comparaison :

```powershell
docker build -f audit/Dockerfile.before -t network-security-tool-api:before .
```

Cette reconstruction utilise les dépendances disponibles au moment où elle est lancée : elle ne garantit pas de retrouver exactement les chiffres historiques.

## Pipelines GitHub Actions

Consulter [les exécutions Actions](https://github.com/YvanDouanla/network-security-tool/actions).

| Workflow | Fichier | Étapes principales | État observé |
|---|---|---|---|
| Python CI and Security | `.github/workflows/ci.yml` | Python 3.12, installation, pytest, Bandit, compilation | Réussi après correction du test volontairement faux |
| Docker image security | `.github/workflows/security-scan.yml` sur la branche Docker | Construction API, export, scan Trivy 0.76.1 | Échec sur **44 HIGH**, code `1` |

Les workflows se déclenchent sur les `push` vers `main` et `feature/**`, et sur les Pull Requests vers `main`. Un même changement peut donc déclencher plusieurs exécutions.

Le contrôle Trivy utilise :

```text
--scanners vuln --severity HIGH,CRITICAL --exit-code 1
```

**Le scan CI est opérationnel, mais l'image ne satisfait pas encore le seuil de sécurité.** Aucune exclusion n'a été ajoutée pour masquer les vulnérabilités sans correctif renseigné.

Un échec empêche normalement les étapes suivantes du même job de s'exécuter. Il ne bloque pas automatiquement tous les jobs indépendants ni la fusion d'une Pull Request : la réussite du contrôle doit être rendue obligatoire dans les règles GitHub pour imposer ce blocage.

## Organisation des fichiers

Cette vue décrit l'ensemble de la branche `feature/docker-security`. Les éléments Docker et `REPONSES_TP3.md` n'existent pas encore dans `main` à l'état documenté.

| Chemin | Contenu |
|---|---|
| `network_check.py` | Fonctions réseau et interface CLI |
| `requirements-dev.txt` | Dépendances pytest et Bandit |
| `tests/test_network_check.py` | Trois tests unitaires |
| `.github/workflows/ci.yml` | CI Python et bonus de compilation |
| `api/main.py` | API FastAPI |
| `api/requirements.txt` | Dépendances API : FastAPI et Uvicorn |
| `api/Dockerfile` | Image API durcie |
| `nginx/default.conf` | Reverse proxy vers `api:8000` |
| `compose.yaml` | Services, réseaux et restrictions d'exécution |
| `.dockerignore` | Exclusions du contexte de construction |
| `.gitignore` | Exclusions Git, notamment `.venv`, caches et archives d'image |
| `.github/workflows/security-scan.yml` | Scan d'image Trivy en CI |
| `audit/` | Rapports, comparaison et configurations initiales |
| `REPONSES.md` | Questions du TP 1 |
| `REPONSES_TP2.md` | Questions du TP 2 et bonus |
| `REPONSES_TP3.md` | Adaptation du sujet, analyse et huit réponses |
| `Captures.pdf` | Pièce de captures ajoutée au dépôt |

## Réponses, preuves et Pull Requests

### Réponses aux questions

- [TP 1 — `REPONSES.md`](https://github.com/YvanDouanla/network-security-tool/blob/main/REPONSES.md)
- [TP 2 — `REPONSES_TP2.md`](https://github.com/YvanDouanla/network-security-tool/blob/main/REPONSES_TP2.md)
- [TP 3 — `REPONSES_TP3.md`](https://github.com/YvanDouanla/network-security-tool/blob/feature/docker-security/REPONSES_TP3.md)
- [Captures PDF présentes dans `main`](https://github.com/YvanDouanla/network-security-tool/blob/main/Captures.pdf)
- [Comparaison Trivy CSV](https://github.com/YvanDouanla/network-security-tool/blob/feature/docker-security/audit/comparaison.csv)

Trois rapports de 25 pages ont également été préparés pendant l'accompagnement. Ils sont des livrables distincts ; ce README ne suppose pas qu'ils ont été ajoutés au dépôt.

### Historique des contributions

| Pull Request | Objet | État documenté |
|---|---|---|
| [PR n° 1](https://github.com/YvanDouanla/network-security-tool/pull/1) | Saisie du port | Fusionnée |
| [PR n° 2](https://github.com/YvanDouanla/network-security-tool/pull/2) | pytest, Bandit et CI | Fusionnée |
| [PR n° 3](https://github.com/YvanDouanla/network-security-tool/pull/3) | Bonus de compilation | Fusionnée |
| [PR n° 4](https://github.com/YvanDouanla/network-security-tool/pull/4) | Docker, durcissement et audit Trivy | Ouverte à l'état documenté ; seuil Trivy non satisfait |

## Incidents rencontrés et corrections

| Symptôme | Cause / diagnostic observé | Correction appliquée |
|---|---|---|
| `Author identity unknown` | Identité Git non configurée | Définir `user.name` et `user.email`, puis relancer le commit |
| Installation PyYAML en échec | Compilation tentée sous Python 3.15, compilateur C++ absent | Utiliser un environnement Python 3.12 pour le TP |
| `No module named pytest` | Utilisation d'un autre interpréteur que `.venv` | Appeler `.\.venv\Scripts\python.exe` explicitement |
| `assert True is False` | Test volontairement incorrect pour le port 443 | Rétablir l'attente `is True`, committer et pousser |
| NGINX ne démarre pas | Montage fichier/dossier incohérent pour `default.conf` | Recréer le fichier, utiliser ASCII et un montage avec `create_host_path: false` |
| Bordures du rapport illisibles | Mauvais décodage UTF-8 | Lire avec `Get-Content -Encoding UTF8` ou exploiter le JSON |
| Faux résultat `after = 0` | Rapport JSON absent | Arrêter sur erreur et vérifier le rapport avant les calculs |
| Job en attente de runner | Machine GitHub non encore attribuée | Attendre le résultat final ; ne pas confondre attente et échec des tests |
| Trivy CI rouge après durcissement | 44 HIGH dépassent encore le seuil | Documenter les résultats et suivre les correctifs ; conserver le contrôle strict |

## Limites et pistes d'amélioration

- Les trois tests actuels ne couvrent pas tous les chemins réseau ni tous les cas de saisie CLI.
- `isinstance(port, int)` accepte aussi les booléens en Python ; la validation stricte de ce cas reste à améliorer.
- Les images de base utilisent des tags et les dépendances des plages de versions : les reconstructions ne sont pas totalement figées. Un verrouillage et des digests vérifiés amélioreraient la reproductibilité.
- Les 44 HIGH résiduelles doivent être suivies et rescannées lors des mises à jour. L'absence de CRITICAL n'est pas une garantie de sûreté globale.
- L'audit présenté vise l'image API. Un audit distinct de NGINX et des configurations compléterait le périmètre.
- Le workflow Bandit du TP 2 analyse `network_check.py` ; il ne couvre pas automatiquement tout le code de l'API ajouté au TP 3.
- L'API est un laboratoire local sans authentification applicative ni TLS configuré. Toute exposition hors du poste nécessiterait une conception et des contrôles supplémentaires.
- Ne jamais committer de mot de passe, jeton ou clé privée. Les rapports d'audit doivent également être relus avant publication.

## Références

- Supports pédagogiques : **TP 1 — Premiers pas avec Git et GitHub**, **TP 2 — GitHub Actions : automatiser les tests et la sécurité**, **TP 3 — NetSecure : audit de sécurité Docker avec Trivy**, Institut F2I / ISRC5.
- [Documentation Git](https://git-scm.com/doc)
- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [Documentation pytest](https://docs.pytest.org/)
- [Documentation Bandit](https://bandit.readthedocs.io/)
- [FastAPI dans Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Docker Compose : réseaux](https://docs.docker.com/compose/how-tos/networking/)
- [Trivy : scan d'images](https://trivy.dev/docs/latest/target/container_image/)

---

**Auteur : Douanla Yvan** · Documentation du parcours de TP des **22 et 23 octobre 2026**.
