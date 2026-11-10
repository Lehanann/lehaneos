# TODO:

Add Pydantic validator to ensure a job defines either:

 - a service
 - or a department

but never neither.

---

Backlog technique
-----------------
- Ajouter un model_validator sur Job
    * service OU department obligatoire
    * service ET department interdits simultanément