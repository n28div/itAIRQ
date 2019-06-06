# Deploy del server
Il deploy del server è stato effettuato sulla piattaforma [Heroku](https://www.heroku.com/) utilizzando il servizio di *continous delivery* fornito dalla piattaforma: ogni volta che un cambiamento viene effettuato al branch `master` heroku si occupa di aggiornare la versione rilasciata del server.

In fase di rilascio è stato necessario settare le variabili `STAGE = prod` che identifica che il server si trova in ambiente di produzione e `FLASK_SECRET_KEY = <secret>` che viene richiesta da Flask.

Differentemente dalla fase di [sviluppo]('/USAGE.md) il server che si occupa di eseguire il codice dell'applicazione non è quello interno di Flask che mal si presta per ambienti di produzioni ma viene bensì utilizzato [gunicorn](https://gunicorn.org/).