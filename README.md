

# Barbershop – Sistema di Prenotazione Online

## Descrizione del Progetto
Barbershop è un’applicazione web dinamica sviluppata con Django 5.x e SQLite, concepita per gestire la prenotazione di servizi in un salone di barbiere. 
Supporta utenti anonimi, clienti registrati e barbers (operatori), con permessi differenziati. Include:

- **Registrazione e login** (anonimi vs. registrati; ruolo cliente vs. barbiere)  
- **Crud dei servizi** (nome, descrizione, prezzo, durata, immagine)  
- **Prenotazioni**: selezione servizio, data/ora, assegnazione barber (manuale o casuale)  
- **Controllo conflitti**: blocco di orari già occupati + suggerimento di fasce libere  
- **Notifiche interne**: messaggi per cliente e barber (non letti evidenziati) quando effettua modifiche prenotazioni
- **Pagine paginate** per servizi e prenotazioni  
- **Back‑office Django Admin** per amministratore  
- **Upload immagini**: avatar utente e foto del servizio  
- **Interfaccia Bootstrap 5** + widget_tweaks per moduli personalizzati  

---

## Tecnologie e Librerie Utilizzate

| Componente        | Versione / Descrizione                               | Motivazione                                    |
|-------------------|------------------------------------------------------|------------------------------------------------|
| **Python**        | 3.13                                                 | Compatibilità con Django 5.x                   |
| **Django**        | 5.x                                                  | Framework “batteries‑included”, ORM, Auth, Admin |
| **SQLite**        | —                                                    | Zero‑config, ideale per sviluppo e demo        |
| **Bootstrap 5**   | CDN                                                  | Layout responsive, componenti già pronti       |
| **django-widget-tweaks** | —                                            | Aggiunta classi CSS ai campi form in template  |
| **django.contrib.messages** | —                                          | Messaggi di conferma/errore nelle view         |

---

## Procedimento

1. Creare e attivare l’ambiente virtuale

    pipenv install
    pipenv shell

2. Applicare le migrazioni

    python manage.py migrate

3. Generare dati di test

    python manage.py generate_test_data

4. Avviare il server

    python manage.py runserver

5. Accedere all’applicazione

    http://127.0.0.1:8000/


---


## Struttura del Progetto

progetto/
├── barbershop_project/      # Configurazione Django (settings, URLs, WSGI)
├── users/                   # App: registrazione, login, Profile
├── services/                # App: CRUD servizi, filtro, paginazione
│   └── management/commands/ # generate_test_data.py
├── appointments/            # App: prenotazioni, conflitti, suggerimenti
├── notifications/           # App: messaggi interni, inbox, mark-as-read
├── templates/               # Template globali e per ogni app
├── static/                  # CSS personalizzato (style.css)
├── media/                   # Upload immagini (avatar, servizi)
├── manage.py                # Script di gestione Django
└── Pipfile


---


## Utilizzo

Anonimi: visualizzano solo lista servizi e filtro.

Registrati (Clienti): possono prenotare un servizio, vedere/modificare le proprie prenotazioni, ricevere notifiche interne.

Barbers: dopo login accedono a “My Services” per creare/aggiornare/cancellare i propri servizi; 
        “My Appointments” per vedere prenotazioni a loro assegnate; 
        ricevono notifiche quando un cliente prenota/modifica/cancella.


---


## test

1. registrazione utente

2. registrazione parrucchiere

3. utente add prenotazione

4. utente add prenotazione su tempo non disponibile (suggestion)

5. parrucchiere add un nuovo servizio