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
- les groupes
- les comptes de service
- les délégations
- les principes d'administration

---

## Informations générales

### Domaine

#### Nom DNS

```text
lehaneos.lan
```

#### NetBIOS

```text
LEHANEOS
```

### Contrôleur de domaine

#### Nom

```text
DC01
```

#### FQDN

```text
DC01.lehaneos.lan
```

#### Système

```text
Windows Server 2022 Core
```

#### Fonctions

- Active Directory Domain Services
- DNS

---

## Structure de l'annuaire

### Organisation

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

---

## Description des OU

### Users

Contient les comptes utilisateurs standards.

Exemples :

```text
ygrondin
jdupont
```

---

### Admins

Contient les comptes d'administration.

Exemples :

```text
ygrondin-adm
```

---

### Service Accounts

Contient les comptes techniques utilisés par les applications.

Exemples :

```text
svc-lehaneos-ldap
svc-lehaneos-ps
```

---

### Servers

Contient les objets ordinateurs des serveurs.

---

### Workstations

Contient les objets ordinateurs des postes de travail.

---

## Groupes

### Departments

Groupes représentant les services métiers de l'organisation.

```text
GRP_DEPT_IT
GRP_DEPT_RH
GRP_DEPT_ACHAT
GRP_DEPT_COMPTA
GRP_DEPT_DIRECTION
```

---

### Shared

Groupes destinés à l'attribution des droits sur les partages réseau.

```text
GRP_SHARE_IT_RH_RW
GRP_SHARE_IT_RH_RO

GRP_SHARE_COMPTA_IT_RW
GRP_SHARE_COMPTA_IT_RO
```

Convention :

```text
RW = Read / Write
RO = Read Only
```

---

### Security

Groupes dédiés à l'administration et aux délégations de sécurité.

```text
GRP_ADM_AD
GRP_ADM_SERVER
GRP_ADM_LEHANEOS
```

---

## Conventions des groupes

### Group Scope

Tous les groupes sont créés avec :

```text
GroupScope : Global
```

#### Justification

L'environnement actuel est composé de :

```text
1 forêt
1 domaine
```

Les groupes globaux sont suffisants et représentent le choix recommandé pour les groupes métier.

---

### Group Category

Tous les groupes sont créés avec :

```text
GroupCategory : Security
```

#### Justification

Les groupes ont vocation à être utilisés pour :

- les ACL NTFS
- les délégations Active Directory
- les partages
- les autorisations applicatives

Les groupes de distribution ne sont actuellement pas utilisés.

---

## Comptes de service

### svc-lehaneos-ldap

#### Fonction

Lecture Active Directory via LDAP.

#### Utilisation

- recherche utilisateur
- recherche groupe
- vérification d'unicité

---

### svc-lehaneos-ps

#### Fonction

Exécution des opérations d'écriture Active Directory.

#### Utilisation

- création utilisateur
- modification utilisateur
- désactivation utilisateur


### Groupes techniques LehanEOS

#### GRP_ADM_LEHANEOS

**Fonction**

Groupe d'administration logique de la plateforme LehanEOS.

**Membres**

```text
svc-lehaneos-ldap
svc-lehaneos-ps
```


**Utilisation**

- Identification des comptes liés à LehanEOS
- Regroupement des comptes techniques
- Audit et traçabilité
- Base des futures délégations

#### GRP_LEHANEOS_LDAP

**Fonction**

Groupe dédié à la lecture de l'annuaire Active Directory.

Membres
```text
svc-lehaneos-ldap
```
**Utilisation**

- Recherche utilisateur
- Recherche groupe
- Vérification d'unicité
- Consultation LDAP

#### GRP_LEHANEOS_PROVISIONING

**Fonction**

Groupe dédié aux opérations de provisioning Active Directory.

Membres
```text
svc-lehaneos-ps
```

**Utilisation**

- Création d'utilisateurs
- Modification d'utilisateurs
- Désactivation d'utilisateurs
- Création de groupes
- Gestion des appartenances aux groupes

---

## Modèle de sécurité

### Principes

- Aucun compte Domain Admin n'est utilisé par l'application.
- Les comptes de service disposent uniquement des droits nécessaires.
- LDAP est utilisé pour les opérations de lecture.
- PowerShell est utilisé pour les opérations d'écriture.

### Source de vérité

Active Directory constitue la source de vérité de la V0.1.

---

## Modèle de délégation

### Principe

Les permissions ne sont jamais attribuées directement aux comptes.

Le modèle retenu est : 

```text 
Utilisateur 
    ↓ 
  Groupe 
    ↓ 
Permissions
```

Cette approche facilite :

- la maintenance
- l'audit
- l'ajout de nouveaux comptes
- le respect du principe du moindre privilège

### GRP_LEHANEOS_LDAP

**Périmètre**

```text
OU=LehanEOS_France
```
**Autorisations cibles**

- Lecture des utilisateurs
- Lecture des groupes
- Lecture des unités organisationnelles

**Restrictions**

- Aucune opération d'écriture
- Aucune création d'objet
- Aucune suppression d'objet
- Aucune modification d'objet

#### GRP_LEHANEOS_PROVISIONING

**Périmètre**

```text
OU=Users
OU=Groups
```

**Autorisations cibles**

- Création d'utilisateurs
- Modification d'utilisateurs
- Désactivation d'utilisateurs
- Création de groupes
- Modification de groupes
- Gestion des appartenances aux groupes

**Restrictions**

- Aucune création d'OU
- Aucune suppression d'OU
- Aucune délégation de droits
- Aucune administration du domaine

#### Administrator

**Périmètre**

```text
Domaine complet
```
**Responsabilités**

- Administration complète du domaine
- Gestion AD DS
- Gestion DNS
- Gestion des délégations
- Restauration et reprise après incident

#### ygrondin-adm

**Périmètre**

Compte d'administration personnel.
Ce compte n'entre pas dans le périmètre fonctionnel de LehanEOS.
Les privilèges associés à ce compte sont définis indépendamment du projet.

---

## État actuel

```text
✅ Domaine créé
✅ OU créées
✅ Groupes créés

⏳ Comptes de service
⏳ Comptes administrateurs dédiés
⏳ Délégations
⏳ LDAP
```

---

## Évolutions prévues

### Futures évolutions

- Délégations d'administration
- Séparation des comptes de provisionnement
- Gestion avancée des groupes
- Microsoft 365
- Automatisation IAM