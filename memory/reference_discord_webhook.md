---
name: discord-webhook-jarvis
description: Webhook Discord pour notifications Jarvis (veille tech, alertes, propositions). Channel #veille-tech sur serveur perso Raphael
type: reference
originSessionId: 42ae4e78-6ae5-48b3-a4f5-f7b07fb3149a
---
Webhook Discord pour envoyer des notifications à Raphael depuis les routines /schedule.

**URL:** `https://discord.com/api/webhooks/1502270441241186375/P44tTDHnpitXv8bn-4VPgS1gTtrbxAyfLVPhDGmh0aSvDyg8okGaMOrL8G3hrTg3GTUn`

**Usage (curl simple, pas d'embeds):**
```bash
curl -s -H "Content-Type: application/json" -d "{\"username\": \"Jarvis\", \"content\": \"MESSAGE ICI\"}" "URL"
```

**Channel:** #veille-tech sur serveur Discord personnel de Raphael
**Username bot:** Jarvis

**IMPORTANT:** Ne JAMAIS commit cette URL dans le repo. Mémoire uniquement.
