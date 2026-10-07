# Ideas
**Document** : IDEAS
**Version** : 1.0 
**Auteur** : Yohan Grondin
**Dernière mise à jour** : 2026-10-07

---

Ce document centralise les idées et pistes d'évolution de LehanEOS.

Aucune fonctionnalité présente dans ce document n'est considérée comme planifiée tant qu'elle n'est pas ajoutée à la roadmap officielle.

---

## Règles

Une idée peut :

- être supprimée
- être fusionnée
- être déplacée vers la roadmap
- ne jamais être développée

La présence d'une idée dans ce document ne constitue pas un engagement de développement.

---

## Core

- Domain Events
- Event Bus interne
- Système de notifications
- Audit centralisé
- Gestion des plugins

### Plugins
- Chargement dynamique des modules
- Architecture plugin
- Marketplace communautaire
- Gestion des dépendances des modules

---

## RH

- Organigramme dynamique
- Gestion des formations
- Suivi des habilitations
- Gestion des compétences
- Gestion des entretiens annuels
- Gestion des arrivées
- Gestion des départs
- Gestion des mutations internes
- Archivage automatique des dossiers
- Génération automatique du dossier employé
- Identifiant RH anonymisé (UUID / HEX64)
- Historisation des changements organisationnels

---

## IAM

- Profils métiers
- Attribution automatique des licences
- Attribution automatique des groupes
- Comptes à durée limitée
- Gestion des prestataires
- Gestion du cycle de vie des identités
- Workflow d'approbation des accès
- Gestion des accès Just-In-Time
- Provisionnement dédié des comptes administratifs

---

## Assets

- Affectation automatique d'un poste
- Affectation automatique d'un téléphone
- Gestion des stocks
- Gestion des seuils d'alerte
- Prévision des achats
- Gestion du cycle de vie du matériel
- Réservation d'équipements

---

## Microsoft 365
 
- Création de comptes
- Attribution automatique des licences
- Gestion des groupes
- Gestion des boîtes partagées
- Création des BAL
- Attribution des rôles
- Gestion des Teams
- Offboarding automatisé

---

## SSAP

- Catalogue applicatif validé par le SI
- Installation à distance
- Désinstallation à distance
- Mise à jour des applications
- Validation des demandes logicielles
- Conformité logicielle
- Détection des logiciels obsolètes
- Détection des logiciels interdits
- Catalogue par métier
- Catalogue par site
- Catalogue par service
- Installation automatique lors de l'affectation d'un poste
- Gestion des versions validées
- Gestion des packages

## Agent SSAP

- Agent Python léger
- Communication MQTT
- Inventaire logiciel local
- Remontée de conformité
- Exécution des installations silencieuses
- Vérification périodique des versions
- Contrôle des logiciels non autorisés
---

## Intégrations

### GLPI

- Synchronisation des actifs
- Réservation de matériel
- Création d'incidents

### ServiceNow

- Création d'incidents
- Gestion des demandes

### Microsoft 365

- Création de boîtes aux lettres
- Attribution de licences

### MQTT

- Communication avec les agents
- Déploiement de logiciels

---

## Reporting

- Dashboard RH
- Dashboard IT
- Dashboard direction
- KPI onboarding

---

## Sécurité

- PKI interne
- Signature des scripts PowerShell
- Bastion d'administration
- PAM
- JIT
- Certification des agents
- Coffre de secrets
- Rotation automatique des certificats
- Audit de conformité

---

## Monitoring

- Monitoring orienté métier
- Réduction du bruit des alertes
- Classification des alertes
- Score de santé du SI
- Corrélation d'événements
- Agrégation d'alertes
- Gestion des faux positifs

## Gouvernance
 
- Audit centralisé
- Historisation des actions
- Validation des workflows
- Gestion des approbations
- Journal des changements
- Traçabilité complète des opérations

---

## ERP / CRM

- Synchronisation ERP
- Synchronisation CRM
- Reporting commercial
- Tableau de bord des commandes

---

## Long terme

- Intranet unifié
- Annuaire d'entreprise
- Portail collaborateur
- Portail manager
- Portail RH
- Portail IT
- Centre de documentation
- Gestion documentaire
- Centre d'annonces internes

## IA
- Assistant d'administration
- Recherche transversale
- Résumé des alertes
- Génération de procédures
- Analyse des tendances
- Recommandations d'onboarding
- Recherche documentaire intelligente
``