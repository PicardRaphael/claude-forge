# Mappings Jira — Types, Request Types et Composants

## issuetype (editJiraIssue)

| Type | ID |
|------|-----|
| Bug | 10004 |
| Support | 10013 |
| Service Request | 10016 |

Identique pour SC (serviceDeskId 1) et SD (serviceDeskId 11).

## customfield_10010 — Type de demande (requestType)

### Projet SC (Syndic)

| Classification | requestType ID |
|---------------|---------------|
| Bug | 6 |
| Support | 19 |
| Service Request | 18 |

### Projet SD (Gerance)

| Classification | requestType ID |
|---------------|---------------|
| Bug | 100 |
| Support | 103 |
| Service Request | 101 |

Format :
```json
{ "customfield_10010": { "requestType": { "id": "[ID]" } } }
```

Si erreur "read-only" → noter dans la note interne "Type de demande a corriger manuellement : [nom cible]". Ne pas bloquer.

## Composants (components)

| Composant | ID |
|-----------|-----|
| CRG | 11079 |
| Appel loyers | 11051 |
| Bail | 11060 |
| Sortie locataire | 11171 |
| Honoraires | 11124 |
| Extranet Syndic | 11094 |
| Extranet Gerance | 11097 |
| Extranet Transversal | 11100 |
| G-Suite | 11117 |
| Drive | 11087 |
| Paiement fournisseur | 11143 |
| Banque | 11057 |
| AG | 11147 |
| Regularisation charges | 11166 |
| Application | 11052 |
| Assurances GLI/GO/PNO | 10370 |

Ajuster le composant via `editJiraIssue` si incorrect par rapport au contenu du ticket.
