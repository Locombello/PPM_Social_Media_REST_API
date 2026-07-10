# Social Media API - Progetto Back-end PPM 2026
**Studente**: Lorenzo Colombani
**Tipo di progetto**: REST API
**Framework utilizzato**: Django / Django REST Framework

### Descrizione del progetto
L'applicazione è una REST API per una piattaforma di Social Media che consente la gestione di post, commenti, interazioni ("mi piace") e relazioni di follow tra utenti. Il sistema implementa una separazione dei permessi basata sui ruoli utente (Utente Standard e Moderatore).

## Database e Account di Demo
Il progetto include un database SQLite pre-popolato denominato db.sqlite3. Al suo interno sono già presenti record di test (post, commenti, interazioni) e i seguenti account demo per la valutazione:

| Username | Password | Ruolo | Descrizione |
| ----------- | ----------- | ----------- | ----------- |
| admin | admin | Superuser / Staff | Superutente che ha accesso completo al pannello di amministrazione. |
| moderator | mod12345 | Standard User | Utente base che può creare post e interagire con altri utenti. |
| user | user12345 | Moderator | Utente avanzato che può rimuovere contenuti inappropriati. |

## Documentazione degli Endpoint API
L'API risponde al prefisso base /api/ e prevede la seguente mappatura:

| Metodo | URL | Autenticazione | Ruolo Consentito | Descrizione |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| POST | /api/token/ | No | Qualsiasi | Effettua il login e restituisce i token JWT (access/refresh). |
| GET | /api/posts/ | Sì | Moderatore | Mostra la lista di tutti i post con i commenti inclusi. |
| POST | /api/posts/ | Sì | Qualsiasi | Consente la creazione di un nuovo post. |
| DELETE | /api/posts/<id>/ | Sì | Utente Standard (Autore) / Moderatore | Cancella un determinato post (consentito solo all'autore o al moderatore).
| POST | /api/comments/ | Sì | Qualsiasi | Rilascia un commento agganciato a un post specifico.

## Flusso di Test con HTTPie
Di seguito sono riportati i comandi per testare il corretto funzionamento dei permessi e dell'autenticazione tramite riga di comando HTTPie:

1. Richiesta del Token JWT (Login):
```
http POST http://127.0.0.1:8000/api/token/ username="user" password="user12345"
```
2. Recupero della lista dei Post (Utilizzando il token ottenuto):

```
http GET http://127.0.0.1:8000/api/posts/ "Authorization: Bearer TOKEN_ACCESS"
```
3. Test Permessi - Cancellazione vietata (Tentare di cancellare un post non proprio con l'utente standard):

```
http DELETE http://127.0.0.1:8000/api/posts/[ID_POST_DI_UN_ALTRO]/ "Authorization: Bearer TOKEN_UTENTE_STANDARD"
# Risposta attesa: 403 Forbidden
```
