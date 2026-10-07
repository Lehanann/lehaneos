# Roadmap LehanEOS
**Document** : ROADMAP
**Version** : 1.0 
**Auteur** : Yohan Grondin
**Dernière mise à jour** : 2026-10-07

---

# Vision

LehanEOS est une plateforme modulaire d'orchestration d'entreprise.

La première brique du projet est un SIRH capable d'automatiser les processus d'intégration et de départ des collaborateurs.

À long terme, LehanEOS a vocation à devenir un portail unifié permettant d'orchestrer différents outils de l'entreprise.

---

# V0.1 - Foundations
## Core

- Initialisation du projet
- Structure modulaire
- Gestion de la configuration
- Logging
- Gestion des exceptions
- PowerShell Runner

## Active Directory

- Connexion LDAP
- Recherche utilisateur
- Recherche groupe
- Vérification d'unicité username
- Vérification d'unicité email

## CLI

- Commande create-user
- Saisie interactive
- Validation des données

## PowerShell

- Création utilisateur AD
- Retour JSON
- Gestion des erreurs

## Infrastructure

- Domaine lehaneos.lan
- Contrôleur de domaine DC01
- Comptes de service

---

# Version 1

## IAM

- Création utilisateur
- Modification utilisateur
- Désactivation utilisateur
- Gestion des groupes
- Gestion des OU

## RH

- Fiche collaborateur
- Gestion documentaire
- Entrées
- Sorties

---

# Version 2

## Microsoft 365

- Création de comptes
- Affectation des licences
- Gestion des groupes
- Archivage des boîtes aux lettres
- Départ des collaborateurs
- Conversion en boîte partagée
- Désactivation des accès

## Assets

- Catalogue matériel
- Attribution de matériel
- Réservation d'un équipement

## Intégration GLPI

- Synchronisation des actifs
- Consultation du parc

---

# Version 3

## SSAP

Self-Service Application Portal

- Catalogue applicatif
- Installation à distance
- Gestion des mises à jour

## MQTT

- Communication avec les agents
- Déclenchement des actions distantes

---

# Version 4

## Automatisation

- APScheduler
- Tâches planifiées
- Workflows automatiques

## Reporting

- KPI RH
- KPI IT
- Dashboards

---

# Version 5

## Intégrations avancées

- ERP
- CRM

---

# Version 6+

## Gouvernance

- Bastion
- Accès JIT
- Audit
- PAM

Ces éléments ne font pas partie du périmètre actuel mais représentent une évolution potentielle de la plateforme.
