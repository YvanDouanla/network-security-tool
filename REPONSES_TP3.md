# TP 3 - Audit Docker et Trivy

Auteur : Douanla Yvan
Projet : network-security-tool

## Adaptation du sujet

Le projet NetSecure initial n'étant pas disponible, ce TP adapte le dépôt network-security-tool des TP 1 et 2. Une API FastAPI réutilise check_port, avec un frontal NGINX et Docker Compose. Aucune base de données n'est nécessaire.

La cible 127.0.0.1 désigne ici le conteneur API, et non le PC Windows.

## Infrastructure

NGINX publie uniquement 127.0.0.1:8080 sur l'hôte.
Il communique avec api:8000 sur le réseau backend.
L'API appartient uniquement au réseau backend, déclaré internal.
NGINX appartient aux réseaux frontend et backend.
La configuration NGINX est montée en lecture seule.
Aucun secret applicatif n'est nécessaire dans cette configuration.

## Résultats avant et après

| Mesure | Avant | Après |
|---|---:|---:|
| HIGH | 434 | 44 |
| CRITICAL | 24 | 0 |
| Total HIGH/CRITICAL | 458 | 44 |
| Espace disque affiché par Docker | 1,64 Go | 201 Mo |
| Utilisateur API | root, UID 0 | appuser, UID 10001 |
| Port API publié sur l'hôte | 8000 | Aucun |

La baisse des occurrences HIGH/CRITICAL est d'environ 90,4 %.
Le total compte des occurrences par paquet et ne représente pas nécessairement des CVE distinctes.

## Trois résultats significatifs du scan initial

| Paquet | Version installée | Sévérité | CVE | Version corrigée |
|---|---|---|---|---|
| libmariadb3 | 1:11.8.6-0+deb13u1 | CRITICAL | CVE-2026-44172 | Non renseignée |
| libxml2-dev | 2.12.7+dfsg+really2.9.14-2.1+deb13u3 | CRITICAL | CVE-2026-6653 | Non renseignée |
| libmariadb-dev-compat | 1:11.8.6-0+deb13u1 | CRITICAL | CVE-2026-49261 | Non renseignée |

Ces informations proviennent du rapport Trivy initial.

## Mesures appliquées

- Remplacement de python:3.12 par python:3.12-slim pour réduire les composants embarqués.
- Exécution de l'API avec un utilisateur non-root, UID 10001.
- Suppression de la publication directe du port API.
- Réseau backend déclaré internal.
- Système de fichiers de l'API en lecture seule, avec /tmp en mémoire.
- Suppression des capacités Linux de l'API avec cap_drop: ALL.
- Activation de no-new-privileges pour l'API.
- Montage NGINX en lecture seule avec create_host_path: false.

Les restrictions d'exécution réduisent les possibilités d'action d'un attaquant, mais ne corrigent pas les CVE des paquets.

## Vérification fonctionnelle

Les deux conteneurs démarrent.
GET /health via NGINX renvoie status: ok.
GET /check?port=8000 renvoie open: true.
La commande id dans le conteneur API confirme UID 10001.

## Résultat du pipeline

Le workflow construit l'image API puis l'analyse avec Trivy 0.76.1.
Le scan CI retrouve 44 HIGH et 0 CRITICAL.
Il échoue avec le code 1 conformément au seuil HIGH,CRITICAL.
Le rapport local ne renseigne aucune version corrigée pour ces 44 occurrences.

Le contrôle est opérationnel, mais l'image ne satisfait pas encore le seuil de sécurité. Les vulnérabilités restantes doivent être suivies et l'image reconstruite puis rescannée à la publication de correctifs. Aucune exclusion n'a été ajoutée pour masquer les résultats.

## Q1. Différence entre scanner le code source et une image Docker ?

Le scan du code source examine les fichiers du projet pour rechercher, selon l'outil, des erreurs de sécurité, des secrets ou des dépendances vulnérables. Le scan d'image analyse les composants réellement embarqués : paquets du système, bibliothèques applicatives et éventuellement configuration ou secrets. Les deux contrôles sont complémentaires.

## Q2. Différence entre un port exposé et un port publié ?

EXPOSE décrit un port utilisé par le conteneur ; il ne le publie pas sur l'hôte et ne constitue pas une règle de pare-feu. La publication avec ports dans Compose ou -p crée un accès via une adresse et un port de l'hôte. Les conteneurs d'un même réseau peuvent communiquer sans publication.

## Q3. Pourquoi isoler une base de données sur backend ?

Cela limite son accès aux services qui en ont besoin et évite une publication inutile sur l'hôte. Cette isolation réduit la surface d'attaque et les possibilités de déplacement latéral. Notre application ne comporte pas de base de données.

## Q4. Risque d'un conteneur exécuté en root ?

Un attaquant qui compromet un processus root dispose de davantage de droits dans le conteneur. Cela augmente les conséquences possibles sur les fichiers, les volumes et, en présence de mauvaises configurations ou de failles, sur l'hôte. Root dans le conteneur ne signifie toutefois pas automatiquement un accès root à l'hôte.

## Q5. Signification de HIGH, CRITICAL, CVE et version corrigée ?

HIGH et CRITICAL sont des niveaux de sévérité, CRITICAL étant plus élevé. Une CVE est un identifiant public de vulnérabilité connue. La version corrigée indique une version du composant contenant un correctif selon la source utilisée. Un champ vide signifie qu'aucune version corrigée n'est renseignée dans le rapport.

## Q6. Que fait --exit-code 1 et pourquoi l'utiliser en CI ?

Cette option demande à Trivy de renvoyer le code 1 lorsque des résultats correspondent aux critères du scan. Avec --severity HIGH,CRITICAL, ces vulnérabilités font échouer l'étape. Les étapes suivantes du même job sont normalement ignorées. Bloquer aussi une fusion nécessite de configurer le contrôle comme obligatoire dans les règles GitHub.

## Q7. Pourquoi une image sans CVE détectée n'est-elle pas nécessairement sûre ?

Le scan dépend de la base de vulnérabilités, de sa date et des composants reconnus. Des failles inconnues, des erreurs applicatives, des secrets ou de mauvaises configurations peuvent subsister. Un résultat nul avec un filtre HIGH,CRITICAL ne signifie pas non plus absence de vulnérabilités de gravité inférieure.

## Q8. Quels risques subsistent après mise à jour des dépendances ?

Des failles inconnues ou sans correctif, des erreurs de logique, des permissions excessives, des secrets divulgués, une mauvaise configuration réseau ou une compromission de la chaîne d'approvisionnement peuvent subsister. Les mises à jour doivent être accompagnées de tests, de durcissement et de scans réguliers.
