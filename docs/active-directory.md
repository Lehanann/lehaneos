# Active Directory

**Document** : ACTIVE-DIRECTORY
**Version** : 1.0
**Auteur** : Yohan Grondin
**Dernière mise à jour** : 2026-10-07

---

## Objectif

Ce document décrit l'architecture Active Directory utilisée par LehanEOS.

L'objectif est de documenter :

- la structure de l'annuaire
- les conventions de nommage
- les comptes de service
- les délégations
- les principes d'administration

---

## Domaine

Nom DNS :

lehaneos.lan

NetBIOS :

LEHANEOS

---

## Contrôleur de domaine

Nom :

DC01

FQDN :

DC01.lehaneos.lan

Système :

Windows Server 2022 Core

Fonctions :

- Active Directory Domain Services
- DNS

Comptes de service

svc-lehaneos-ldap
    Lecture LDAP

svc-lehaneos-ps
    Opérations PowerShell AD

---

## Structure de l'annuaire

Organisation : 

```text
DC=lehaneos,DC=lan

└── OU=LehanEOS_France

    ├── OU=Users

    ├── OU=Admins

    ├── OU=Service Accounts

    ├── OU=Servers

    ├── OU=Workstations

    └── OU=Groups

        ├── OU=Departments

        ├── OU=Shared

        └── OU=Security
```
>### Description des OU 

### 1. Users 

Comptes utilisateurs standards. 

Exemple : 
- ygrondin 
- jdupont 

### 2. Admins 
Comptes d'administration. 

Exemple : 

- ygrondin-adm 

### 3. Service Accounts

Comptes techniques utilisés par les applications. 

Exemple : 

- svc-lehaneos-ldap 
- svc-lehaneos-ps 

### 4. Servers 
Objets ordinateurs des serveurs. 

### 5. Workstations** 

Objets ordinateurs des postes de travail.

>### Groupes

### 1. **Departments**

Groupes représentant les services métiers.

Exemples :

- GRP_DEPT_IT
- GRP_DEPT_RH
- GRP_DEPT_ACHAT
- GRP_DEPT_COMPTA

### 2. **Shared**

Groupes d'accès aux partages.

Exemples :

- GRP_SHARE_IT_RW
- GRP_SHARE_IT_RO

### 3. **Security**

Groupes de sécurité et d'administration.

Exemples :

- GRP_ADM_AD
- GRP_ADM_SERVER
- GRP_ADM_LEHANEOS

>### Comptes de service

### 1. svc-lehaneos-ldap

Fonction :

Lecture Active Directory via LDAP.

Utilisation :

- Recherche utilisateur
- Recherche groupe
- Vérifications d'unicité

### 2. svc-lehaneos-ps

Fonction :

Exécution des opérations d'écriture Active Directory.

Utilisation :

- Création utilisateur
- Modification utilisateur
- Désactivation utilisateur

>### Modèle de sécurité
### 1. Principes

- Aucun compte Domain Admin utilisé par l'application.
- Les comptes de service disposent uniquement des droits nécessaires.
- LDAP est utilisé pour les opérations de lecture.
- PowerShell est utilisé pour les opérations d'écriture.

>### Source de vérité

Active Directory constitue la source de vérité de la V0.1.

>### Évolutions prévues

### 1. Futures évolutions
- Délégations d'administration
- Séparation des comptes de provisionnement
- Microsoft 365
- Gestion avancée des groupes
