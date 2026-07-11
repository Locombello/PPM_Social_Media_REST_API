# Social Media API - Progetto Back-end PPM 2026
**Studente**: Lorenzo Colombani
**Tipo di progetto**: REST API
**Framework utilizzato**: Django / Django REST Framework

### Descrizione del progetto
L'applicazione è una REST API per una piattaforma di Social Media che consente la gestione di post, commenti e like oltre che alla registrazione di utenti e alla gestione delle relazioni di follow tra essi. Il sistema implementa una separazione dei permessi basata sui ruoli utente (Utente Standard e Moderatore) e un'autenticazione *stateless* basata su token JWT con gestione del logout tramite Blacklist.

## Funzionalità Implementate per Ruolo
L'applicazione fornisce una serie di funzionalità in base allo stato di autenticazione dell'utente e al suo ruolo. Di seguito elencate le funzionalità raggruppate per ruolo. Le funzionalità fornite ad un tipo di utente ad una certa posizione dell'elenco sono ereditate anche da tutti gli altri utenti sottostanti.

### Utente Non Autenticato (Guest)
*   **Registrazione:** Creazione di un nuovo account utente.
*   **Autenticazione:** Login tramite credenziali per ottenere Access e Refresh Token (JWT).
*   **Refresh:** Rinnovo del token di accesso scaduto.

### Utente Standard
*   **Logout:** Logout sicuro con invalidazione del token tramite Blacklist.
*   **Profili:** Visualizzazione dei dettagli del profilo di un utente tramite username.
*   **Gestione dei Follow:** 
    *   Visualizzazione della lista di utenti seguiti e dei propri follower.
    *   Follow e Unfollow di un utente.
    *   Rimozione forzata di un follower dalla propria lista di follower.
*   **Gestione dei Post:**
    *   Visualizzazione del feed globale.
    *   Visualizzazione del feed personale (post dei soli seguiti).
    *   Visualizzazione del proprio profilo e creazione di nuovi post.
    *   Modifica ed eliminazione esclusiva dei *propri* post.
*   **Gestione dei Commenti:**
    *   Visualizzazione della cronologia dei commenti lasciati sui post.
    *   Visualizzazione della sezione commenti di un post e creazione di un nuovo commento.
    *   Modifica ed eliminazione esclusiva dei *propri* commenti sotto a un post.
*   **Gestione dei Like:**
    *   Visualizzazione della cronologia dei post a cui si ha lasciato like.
    *   Aggiunta e rimozione di un like su un post.

### Moderatore (Staff)
*   **Moderazione Contenuti:** Diritto di eliminare post o commenti creati da *qualsiasi* utente, al fine di mantenere la community sicura e rispettosa delle linee guida.

### Amministratore (Superuser)
*   **Amministrazione:** Accesso completo al pannello di amministrazione nativo di Django per la gestione diretta del database e l'assegnazione dei ruoli.

## Istruzioni per l'Installazione Locale
1. **Clona il repository:**
    ```bash
    git clone git@github.com:Locombello/PPM_Social_Media_REST_API.git
2. **Crea e attiva un ambiente virtuale (anaconda):**
    ```bash
    cd PPM_Social_Media_REST_API
    conda create -n social_media
    conda activate social_media
3. **Installa le dipendenze:**
    ```bash
    pip install -r requirements.txt
4. **Applica le migrazioni:**
    ```bash
    python manage.py migrate
5. **Avvia il server:**
    ```bash
    python manage.py runserver
L'API sarà ora in ascolto all'indirizzo: http://127.0.0.1:8000/

## Database e Account di Demo
Il progetto include un database SQLite pre-popolato con dati di demo denominato db.sqlite3. Al suo interno sono già presenti record di test (post, commenti, interazioni) e i seguenti account demo per la valutazione:

| Username | Password | Ruolo | Descrizione |
| ----------- | ----------- | ----------- | ----------- |
| admin | admin | Superuser / Staff | Superutente che ha accesso completo al pannello di amministrazione. |
| moderator | mod12345 | Standard User | Utente avanzato che può rimuovere contenuti inappropriati. |
| user | user12345 | Moderator | Utente base che può creare post e interagire con altri utenti. |

## Online Deployment
L'API è stata distribuita ed è pubblicamente accessibile al seguente link:
[link al deploy]

## Documentazione degli Endpoint
Di seguito la mappatura completa di tutti gli endpoint esposti dall'API. Il prefisso base per tutte le rotte è `/api/`.

### Autenticazione e Registrazione
| Metodo | URL | Auth | Ruolo | Request Body | Esempio Risposta | Descrizione |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **POST** | `/register/` | No | Qualsiasi | `username`, `email`, `password` | `201 Created` | Registra un nuovo utente. |
| **POST** | `/login/` | No | Qualsiasi | `username`, `password` | `200 OK` | Login: restituisce i token `access` e `refresh`. |
| **POST** | `/login/refresh/` | No | Qualsiasi | `refresh` | `200 OK` | Rinnova l'access token scaduto. |
| **POST** | `/logout/` | Sì | Qualsiasi | `refresh` | `205 Reset Content` | Invalida il refresh token inserendolo in blacklist. |

### Gestione Utenti e Follow
| Metodo | URL | Auth | Ruolo | Request Body | Esempio Risposta | Descrizione |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GET** | `/users/<username>/` | Sì | Qualsiasi | - | `200 OK` | Mostra i dettagli del profilo di un utente specifico. |
| **GET** | `/users/following/` | Sì | Qualsiasi | - | `200 OK` | Lista degli utenti che l'utente corrente sta seguendo. |
| **POST** | `/users/following/` | Sì | Qualsiasi | `user_id` | `201 Created` | Inizia a seguire l'utente specificato. |
| **GET** | `/users/following/<id>/` | Sì | Qualsiasi | - | `200 OK` | Verifica se si segue un determinato utente. |
| **DELETE**| `/users/following/<id>/` | Sì | Qualsiasi | - | `204 No Content` | Smette di seguire l'utente specificato. |
| **GET** | `/users/followers/` | Sì | Qualsiasi | - | `200 OK` | Lista degli utenti che seguono l'utente corrente. |
| **GET** | `/users/followers/<id>/` | Sì | Qualsiasi | - | `200 OK` | Dettaglio di un proprio follower specifico. |
| **DELETE**| `/users/followers/<id>/` | Sì | Qualsiasi | - | `204 No Content` | Rimuove l'utente dalla propria lista di follower. |

### Post e Feed
| Metodo | URL | Auth | Ruolo | Request Body | Esempio Risposta | Descrizione |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GET** | `/posts/` | Sì | Qualsiasi | - | `200 OK` | Feed globale contenente tutti i post. |
| **GET** | `/posts/personal_feed/` | Sì | Qualsiasi | - | `200 OK` | Feed personalizzato coi post degli utenti seguiti. |
| **GET** | `/posts/profile/` | Sì | Qualsiasi | - | `200 OK` | Mostra solo i post creati dall'utente corrente (profilo). |
| **POST** | `/posts/profile/` | Sì | Qualsiasi | `content` | `201 Created` | Crea un nuovo post. |
| **GET** | `/posts/<id>/` | Sì | Qualsiasi | - | `200 OK` | Mostra i dettagli di un singolo post. |
| **PATCH**| `/posts/<id>/` | Sì | Autore / Mod | `content` | `200 OK` | Aggiorna parzialmente un proprio post. |
| **DELETE**| `/posts/<id>/` | Sì | Autore / Mod | - | `204 No Content` | Elimina un post specifico. |

### Commenti
| Metodo | URL | Auth | Ruolo | Request Body | Esempio Risposta | Descrizione |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GET** | `/comments/history/` | Sì | Qualsiasi | - | `200 OK` | Storico di tutti i commenti scritti dall'utente. |
| **GET** | `/posts/<post_id>/comments/` | Sì | Qualsiasi | - | `200 OK` | Lista dei commenti sotto a un post specifico. |
| **POST** | `/posts/<post_id>/comments/` | Sì | Qualsiasi | `content` | `201 Created` | Aggiunge un commento al post. |
| **GET** | `/posts/<post_id>/comments/<id>/` | Sì | Qualsiasi | - | `200 OK` | Mostra il dettaglio di un singolo commento. |
| **PATCH**| `/posts/<post_id>/comments/<id>/` | Sì | Autore / Mod | `content` | `200 OK` | Aggiorna parzialmente un proprio commento. |
| **DELETE**| `/posts/<post_id>/comments/<id>/` | Sì | Autore / Mod | - | `204 No Content` | Elimina un commento specifico. |

### Like
| Metodo | URL | Auth | Ruolo | Request Body | Esempio Risposta | Descrizione |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GET** | `/likes/` | Sì | Qualsiasi | - | `200 OK` | Storico di tutti i post a cui l'utente ha messo like. |
| **POST** | `/posts/<post_id>/like/` | Sì | Qualsiasi | - | `200 OK` / `201` | Aggiunge o rimuove un like al post (Toggle). |

## Flusso di Test con HTTPie
Per testare le API da riga di comando in modo semplice e leggibile, si consiglia l'utilizzo di **HTTPie**.

*   **Link di installazione:** [https://httpie.io/cli](https://httpie.io/cli)
*   **Base URL Locale:** `http://127.0.0.1:8000/api/`

### 1. Registrazione di un nuovo account
Crea un nuovo utente fornendo username, email e password.
```bash
http POST http://127.0.0.1:8000/api/register/ username="nuovoutente" email="nuovo@example.com" password="PasswordSicura123"
```

### 2. Effettuare il Login (Ottenere i Token)
Usa le credenziali appena create (o quelle di demo) per ottenere il token JWT di accesso e di refresh.
```bash
http POST http://127.0.0.1:8000/api/login/ username="user" password="user12345"
```
*Copia il valore del campo `"access"` restituito nella risposta JSON. Per tutte le rotte protette, devi includere l'access token nell'header `Authorization` preceduto dalla parola `Bearer`.*

### 3. Esempi di Operazioni Principali

**Leggere il feed globale dei post:**
```bash
http GET http://127.0.0.1:8000/api/posts/ "Authorization: Bearer TUO_TOKEN_ACCESS_QUI"
```

**Creare un nuovo Post:**
Passa il contenuto del post nel body della richiesta.
```bash
http POST http://127.0.0.1:8000/api/posts/ "Authorization: Bearer TUO_TOKEN_ACCESS_QUI" content="Questo è il mio primo post da HTTPie!"
```

**Aggiungere (o rimuovere) un Like a un post (Toggle):**
Esempio su un post con ID = 1.
```bash
http POST http://127.0.0.1:8000/api/posts/1/like/ "Authorization: Bearer TUO_TOKEN_ACCESS_QUI"
```

**Iniziare a seguire un utente:**
Aggiungi un utente (es. ID = 2) alla tua lista dei seguiti.
```bash
http POST http://127.0.0.1:8000/api/users/following/ "Authorization: Bearer TUO_TOKEN_ACCESS_QUI" user_id=2
```

**Smettere di seguire un utente:**
Usa il metodo DELETE sulla rotta di dettaglio.
```bash
http DELETE http://127.0.0.1:8000/api/users/following/2/ "Authorization: Bearer TUO_TOKEN_ACCESS_QUI"
```

**Pubblicare un Commento su un Post:**
Esempio per commentare il post con ID = 1.
```bash
http POST http://127.0.0.1:8000/api/posts/1/comments/ "Authorization: Bearer TUO_TOKEN_ACCESS_QUI" content="Bel post, sono d'accordo!"
```

### 4. Testare i Permessi e i Ruoli

**Tentativo di eliminazione vietata (Errore 403 Forbidden):**
Prova a eliminare un post di un altro utente usando un account di tipo *Utente Standard*.
```bash
http DELETE http://127.0.0.1:8000/api/posts/5/ "Authorization: Bearer TOKEN_UTENTE_STANDARD_QUI"
```
*Risposta attesa: L'API bloccherà la richiesta restituendo `403 Forbidden`.*

### 5. Effettuare il Logout (Blacklist)
Per chiudere la sessione, invia il Refresh Token in modo che venga invalidato.
```bash
http POST http://127.0.0.1:8000/api/logout/ "Authorization: Bearer TUO_TOKEN_ACCESS_QUI" refresh="TUO_TOKEN_REFRESH_QUI"
```
*Risposta attesa: `205 Reset Content`. Se provi a usare di nuovo quel refresh token per ottenere nuovi accessi, riceverai un errore `401 Unauthorized`.*