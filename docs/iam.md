# Identity & Access Management

**Document** : IAM  
**Version** : 1.0  
**Auteur** : Yohan Grondin  
**Dernière mise à jour** : 2026-11-19

---

## Objectif
Le domaine IAM de LehanEOS permet la gestion
du cycle de vie des comptes Active Directory.

Les opérations sont validées en Python
avant exécution PowerShell.

---

## Architecture 
```text 
CLI 
↓
IAM Services
↓
LDAP Validation
↓
PowerShell Execution
↓
Active Directory
```

---

## User Lifecycle
```text
Create
↓
Enabled User
↓
Disable
↓
OU=Disabled
↓
Enable
ou
Delete
```

---

## Create User
Entrées:
```text
Prénom
Nom
Métier
```

Sorties:
```text
Compte AD
Groupes
Email
```

---

## Disable User
Conditions:
```text
Utilisateur existant
Compte actif
```
Actions:
```text
Disable-ADAccount
Move-ADObject -> OU Disabled
```

---

## Enable User
Conditions:
```text
Utilisateur désactivé
Compte situé dans OU Disabled
```
Actions:
```text
Move-ADObject -> OU Users
Enable-ADAccount
```

---

## Delete User
Conditions :
```text
Compte désactivé
Compte situé dans OU Disabled
```
Actions :
```text
Remove-ADUser
```

---

## Reset Password

Conditions:
```text
Utilisateur existant
```

Actions:
```text
Generate Temporary Password
Set-ADAccountPassword
```
---

## Règles métier

- Un compte actif ne peut pas être supprimé.
- Une désactivation entraîne automatiquement
le déplacement du compte vers OU=Disabled.
- Un compte doit être déplacé vers OU=Disabled
avant suppression.
- Une réactivation n'est possible que depuis
OU=Disabled.


## Version History

|Version | Description |
|--- | --- |
| 1.0 | Active Directory User Lifecycle |