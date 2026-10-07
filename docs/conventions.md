
# Conventions de développement
**Document** : CONVENTIONS
**Version** : 1.0 
**Auteur** : Yohan Grondin
**Dernière mise à jour** : 2026-10-07

## Objectif

Ce document définit les conventions techniques du projet LehanEOS.

L'objectif est de garantir la cohérence du code, de la documentation et de l'architecture sur le long terme.

---

# Langue
## Documentation
Toute la documentation est rédigée en français.

Exemples :
- README.md
- roadmap.md
- architecture.md
- active-directory.md

## Code
Tout le code source est rédigé en anglais

Exemples :
- classes
- fonctions
- variables
- constantes
- exceptions

## Docstrings
Toutes les docstrings sont rédigée en anglais.

## Commentaires
Les commentaires techniques sont rédigés en anglais.

---

# Nommage

## Fichiers python

Convention : 

>snake_case

Exemples :
- user_service.py
- active_directory_client.py
- powershell_runner.py

## Fonctions

Convention :

>snake_case

Exemples :

- create_user()
- search_user()
- username_exists()

## Classes

Convention :

>PascalCase

Exemples :
- UserService
- ActiveDirectoryClient
- PowershellRunner

## Variables

Convention :

>snake_case

Exemples :
- first_name
- last_name
- username

## Constantes

Convention :

>UPPER_CASE

Exemples :
- DEFAULT_TIMEOUT
- LDAP_PORT

---

# Git

## Branche principale

main

## Commits

Les commits doivent être atomiques.

Une fonctionnalité = un commit.

Exemples :
- feat: add username generation
- feat: add LDAP user search
- fix: handle duplicate usernames
- docs: update active directory documentation

---

# Structure du projet
Le code python se trouve exclusivement dans :
```text
src/lehaneos
```

Toute nouvelle fonctionnalité doit être organisée par domaine métier ou intégration.

---

# Documentation

Toute décision d'architecture importante doit être documentée dans le dossier :
```text
docs/
```

Exemples :
- ajout d'une intégration 
- changement d'architecture
- évolution de l'infrastructure

---

# Active Directory

## Domaine
```text
lehaneos.lan
```
## Contrôleur de domaine principal
```text
DC01.lehaneos.lan
```
## NetBIOS
```text
LEHANEOS
```

---

# Philosophie
Python = orchestration

Powershell = exécution

LDAP = lecture

Le métier doit rester dans Python.

Les intégrations ne doivent jamais contenir de logique métier.

---

# Règles d'architecture

## Ne pas sur-ingénier

Un dossier ou une couche technique ne doit être créé que lorsqu'un besoin réel apparaît.

## Source de vérité

V0.1 :
Active Directory est la seule source de vérité.

## Priorité

Valider un cas d'usage complet avant d'ajouter une nouvelle technologie.