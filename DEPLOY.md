# Deploy del server
Il deploy del server è stato effettuato sulla piattaforma [Heroku](https://www.heroku.com/) utilizzando il servizio di *continous delivery* fornito dalla piattaforma: ogni volta che un cambiamento viene effettuato al branch `master` heroku si occupa di aggiornare la versione rilasciata del server.
Tuttavia il deploy viene effettuato solamente in caso la API fornisca dati esatti: il servizio [Travis-CI](https://travis-ci.org/n28div/itAIRQ) si occupa di eseguire la suite di *test* (presenti nella cartella [tests](./tests)) utilizzando la libreria standard di python `unittest`.

In fase di rilascio in produzione è necessario settare le seguenti variabili di sistema

|Var|Valore|Descrizione|
|---|---|---|
|`STAGE`|`prod`|Il server è in produzione
|`FLASK_SECRET_KEY`|`<secret>`|Stringa pseudocasuale utilizzata da Flask per criptare per es. `sessionid`
|`REDISCLOUD_URL`|`<url redis>`|Indirizzo in cui è presente il server Redis (comprensivo di username e password)

Differentemente dalla fase di [sviluppo]('/USAGE.md) il server che si occupa di eseguire il codice dell'applicazione non è quello interno di Flask che mal si presta per ambienti di produzioni ma viene bensì utilizzato [gunicorn](https://gunicorn.org/).