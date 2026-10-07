# LehanEOS

Infrastructure & Automation Platform

## Présentation

LehanEOS est une plateforme modulaire d'orchestration du système d'information.

L'objectif du projet est de centraliser et d'automatiser différents processus métiers et techniques au travers d'une architecture modulaire.

LehanEOS n'a pas vocation à remplacer les solutions existantes telles que :

- Active Directory
- Microsoft 365
- GLPI
- ERP
- CRM

Le projet agit comme une couche d'orchestration entre les différents systèmes.

---

## Philosophie

LehanEOS repose sur les principes suivants :

- Python = orchestration
- PowerShell = exécution
- LDAP = lecture
- Connecteurs = intégrations externes

La logique métier doit rester dans Python.

---

## État du projet

Version actuelle :

```text
V0.1 - Foundations
```

Objectif actuel :
```text
Valider les fondations techniques du projet.
```
Technologies utilisées :

- Python
- Typer
- LDAP3
- PowerShell
- Active Directory

Éléments volontairement exclus :

- Base de données
- API REST
- Frontend
- MQTT
- Microsoft 365
- GLPI

## Premier cas d'usage

Commande cible :
```text
lehaneos create-user
```

Fonctionnalités :

- Validation des données
- Génération du login
- Génération de l'adresse email
- Vérification LDAP
- Création du compte Active Directory

---

## Architecture
```text
Utilisateur
↓
CLI
↓
Python
↓
LDAP
↓
PowerShell
↓
Active Directory
```

---

## Documentation
La documentation du projet est disponible dans le dossier :
```text
docs/
```

Documents principaux :

- architecture.md
- roadmap.md
- conventions.md
- active-directory.md
- security.md
- ideas.md

---

## Roadmap

Les évolutions du projet sont décrites dans :

```text
docs/roadmap.md
```

## Licence

Projet personnel en cours de développement.