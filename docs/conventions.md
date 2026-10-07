
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

## Compte utilisateur

jdoe

Exemple:
```text
Philippe Martin = pmartin
Jean Dupont = jdupont
```


## Comptes administrateur

[login]-adm

Exemple :

```text
pmartin-adm
jdupont-adm
```

## Comptes de services

svc-[application]-[role]

Exemple :

```text
svc-lehaneos-ldap
svc-lehaneos-ps
svc-backup
```

## Groupes de départements

GRP_DEPT_[SERVICE]

Exemple :
```text
GRP_DEPT_IT
GRP_DEPT_ACHAT
GRP_DEPT_COMPTA
```

## Groupes de partage

GRP_SHARE_[SERVICE/NOM_DU_REPERTOIRE]_[DROIT]

Exemple :
```text
GRP_SHARE_IT_RW
GRP_SHARE_IT_RO

GRP_SHARE_RH_IT_RO
GRP_SHARE_RH_IT_RW
```

## Groupes de Sécurité

GRP_ADM_[ROLE]

```text
GRP_ADM_AD
GRP_ADM_SERVER
GRP_DEV_SERVER
```

## OU
```text
Users
Admins
Service Accounts
Servers
Workstations
```
Pas besoin de prefixe.

Les OU doivent rester lisibles.

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