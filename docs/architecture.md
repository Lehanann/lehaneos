# Architecture LehanEOS
**Version** : 1.0 
**Auteur** : Yohan Grondin
**Dernière mise à jour** : 2026-10-07

---

## Vision

LehanEOS est une plateforme modulaire d'orchestration d'entreprise.

L'objectif est de fournir un socle permettant d'intégrer progressivement
plusieurs domaines métiers :

- Identity & Access Management (IAM)
- Ressources Humaines (RH)
- Self-Service Application Portal (SSAP)
- Gestion des actifs
- Intégrations externes

LehanEOS n'a pas vocation à remplacer les solutions existantes
(Active Directory, GLPI, ERP, CRM, etc.) mais à les orchestrer au travers
d'une expérience utilisateur unique.

La première étape du projet consiste à valider les fondations techniques de la plateforme au travers d'un premier cas d'usage IAM basé sur Active Directory.

---

## Principes d'architecture

### Architecture modulaire

Le projet adopte une architecture orientée domaine (Domain Based Architecture).

Chaque domaine métier possède son propre espace :

- **iam/**
- **rh/**
- **ssap/**
- **assets/**

Chaque module est responsable de ses composants métier et de ses intégrations.

Cette approche facilite :

- la maintenance
- les évolutions futures
- la séparation des responsabilités
- l'ajout de nouveaux modules

### Pourquoi une architecture par domaine ?

Deux approches ont été étudiées :

#### Architecture par couches
```text
api/
services/
repositories/
models/
```

Cette approche est adaptée aux applications simples reposant
sur un périmètre métier unique.

#### Architecture par domaine
```text
rh/
iam/
assets/
```

Cette approche est privilégiée dans LehanEOS car le projet a
vocation à accueillir plusieurs domaines métiers indépendants.

Chaque module reste autonome et peut évoluer sans impact
important sur les autres modules.

---

## Architecture V0.1

La version 0.1 a pour objectif de valider les fondations techniques du projet.

Technologies retenues :

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

L'objectif est de valider un premier flux complet :

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

## Structure du projet
```text
LehanEOS/
├── docs/
│   ├── roadmap.md
│   ├── conventions.md
│   ├── architecture.md
│   ├── security.md
│   └── active-directory.md
├── src/
│   └── lehaneos/
|       ├── cli/
│       ├── core/
│       │   ├── logging.py
│       │   └── powershell_runner.py
|       ├── integrations/
|       |    └──  active_directory/ Cette structure représente la version 0.1 du projet. Les modules métier seront introduits progressivement selon la roadmap.
│       ├── settings/
│       │   └── config.py
|       ├── utils/
│       └── main.py
├── tests/
├── scripts/
│   └── powershell/
├── .env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Évolution prévue

### V0.1

- Core
- Active Directory
- LDAP
- PowerShell
- CLI

### V1

- IAM
- RH

### V2

- Assets
- GLPI
- Microsoft 365

### V3

- SSAP
- MQTT

### V4

- Automatisation
- Reporting

### V5

- Gouvernance

---

## Séparation des responsabilités

Python :
Logique métier et orchestration.

PowerShell :
Exécution des actions système.

LDAP :
Lecture et contrôle des données Active Directory.

Active Directory :
Source de vérité de la V0.1.

Connecteurs :
Couche d'intégration vers les systèmes externes.

---

## Règles d'architecture

- Aucun composant ne doit être introduit avant qu'un besoin réel ne soit identifié.
- La V0.1 privilégie la simplicité à la complétude fonctionnelle.
- Une fonctionnalité doit être validée de bout en bout avant l'introduction d'une nouvelle technologie.
- Le code métier ne doit pas dépendre directement d'une intégration externe.
- Les échanges avec Active Directory passent par le module integrations.
- Les échanges avec GLPI passent par le module integrations.
- Les modules métier doivent rester indépendants.
- Les services ne doivent pas accéder directement à la base de données.
- Les accès aux données passent par les repositories.
