# LehanEOS

Infrastructure & Automation Platform
Identity & Access Management v1.0

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
V1.0.0 - Identity & Access Management
```

Objectif atteint :
```text

Livraison du premier domaine métier complet de LehanEOS :
Identity & Access Management (IAM) pour Active Directory.

Le projet permet désormais la gestion du cycle de vie utilisateur :
création, désactivation, réactivation, suppression contrôlée et
réinitialisation des mots de passe.
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

Fonctionnalités :

- Validation des données
- Génération du login
- Génération de l'adresse email
- Vérification LDAP
- Création du compte Active Directory
- Désactivation avec déplacement vers l'OU Disabled
- Réactivation avec restauration vers l'OU Users
- Suppression sécurisée des comptes désactivés
- Réinitialisation de mot de passe
---

## Active Directory IAM
### User Lifecycle

- Create user account
- Disable user account
- Enable user account
- Delete disabled user account
- Reset user password

#### Validations

- LDAP user existence validation
- LDAP group validation
- LDAP organizational unit validation
- Disabled account validation
- Organizational unit lifecycle validation

Commande disponibles :
```text
lehaneos user create
lehaneos user disable
lehaneos user enable
lehaneos user delete
lehaneos user reset-password
```

---

## Architecture
```text
Operator
↓ 
CLI (Typer)
↓
IAM Domain Services
↓
LDAP / Repositories
↓
PowerShell Runner
↓
Active Directory
```

---

## Prochaine étape
V1.1 - Resource Provisioning

Objectifs :

- SMB Share Provisioning
- SMB Share Lifecycle Management
- Security Group Automation

Future domains:

- SIRH
- SSAP
- Microsoft 365
- FastAPI
- Next.js

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

Projet personnel en développement actif.