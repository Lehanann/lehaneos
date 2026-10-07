# ADR-001

## Statut

Accepté

## Décision

Utilisation de LDAP3 pour les opérations de lecture Active Directory.

## Contexte

LehanEOS utilise Active Directory comme source de vérité.

Les opérations suivantes doivent être réalisées depuis Python :

- recherche utilisateur
- recherche groupe
- vérification d'unicité
- validation des données

LDAP3 permet d'effectuer ces opérations sans dépendre de PowerShell.

## Conséquences

- LDAP devient la couche de lecture Active Directory.
- Les contrôles métier restent dans Python.
- Les opérations d'écriture ne sont pas concernées.

---

# ADR-002

## Statut

Accepté

## Décision

PowerShell est utilisé pour les opérations d'écriture Active Directory.

## Contexte

Les opérations suivantes nécessitent une modification d'Active Directory :

- création utilisateur
- modification utilisateur
- désactivation utilisateur
- gestion des groupes

Les cmdlets Active Directory fournies par Microsoft représentent la méthode native d'administration.

## Conséquences

- Python orchestre les traitements.
- PowerShell exécute les actions système.
- Les scripts doivent retourner un format standardisé (JSON).

---

# ADR-003

## Décision

Active Directory est la source de vérité de la V0.1.

## Contexte

Le projet ne possède pas encore de base de données.

Toutes les informations utilisateurs sont stockées dans Active Directory.

## Conséquences

- Aucun stockage local n'est introduit.
- PostgreSQL est reporté à une version ultérieure.
- LDAP et Active Directory sont les seules sources de données.

---

# ADR-004

## Décision

La version 0.1 privilégie la validation des fondations techniques.

## Contexte

Le projet possède une vision long terme importante :

- RH
- IAM
- Assets
- SSAP
- Gouvernance

Le risque est d'introduire trop tôt des composants inutiles.

## Conséquences

Les éléments suivants sont exclus de la V0.1 :

- PostgreSQL
- API REST
- Frontend
- MQTT
- GLPI
- Microsoft 365

L'objectif unique est la validation du flux :

CLI → Python → LDAP → PowerShell → Active Directory