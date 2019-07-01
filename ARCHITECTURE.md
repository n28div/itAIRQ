# Architettura adottata
L'API è stata scritta utilizzando il linguaggio *Python* e si divide in tre *"macro-componenti"* differenti:
 * [I componenti che si occupano di reperire i dati](#scaricamento-dei-dati)
 * [Il componente che si occupa di aggregare tutti i dati di tutte le regioni e fornirli tramite l'API RESTful](#server-http)
 * [Il sistema di *caching*](#caching) che lavora in stretto contatto con i due componenti

## Scaricamento dei dati
Lo scaricamento dei dati viene effettuato diversamente per ogni regione poiché ogni regione fornisce diversamente i propri dati.

Per far si che l'API possa lavorare con un interfaccia omogenea ogni regione è una classe derivata da [`BaseRegion`](regions/region.py).

L'implementazione di una regione consiste nell'overriding del metodo costruttore (`__init__`) in cui vengono registrate le province di una regione e nell'overriding del metodo `_fetch_air_quality_routine` in cui viene implementata la routine di scaricamento e manipolazione dei dati presi dalle varie regioni. Esso viene effettuato su un thread separato così da poter effettuare lo scaricamento di più regioni in parallelo.

Le librerie utilizzate in questa fase sono:
 * [requests](https://3.python-requests.org/) utilizzata per effettuare richieste HTTP
 * [BeutifulSoup 4](https://www.crummy.com/software/BeautifulSoup/) utilizzata per lo scraping delle pagine HTML nel caso esso fosse necessario
 * [html-table-extractor](https://github.com/yuanxu-li/html-table-extractor) per effettuare una gestione a più alto livello delle tabelle HTML
 * [sodapy](https://github.com/xmunoz/sodapy) utilizzato per le regioni che offrono i propri dati come Open Data utilizzando [Socrata](https://www.tylertech.com/products/socrata)

## Server HTTP
Il server HTTP RESTful è stato sviluppato utilizzando la libreria [Flask](http://flask.pocoo.org/).
Esso si occupa di aggregare i dati forniti da ogni [`BaseRegion`](regions/region.py) e di renderli disponibili attraverso richieste HTTP. 
La documentazione delle richieste HTTP è reperibile alla [pagina dedicata](./API.md).
L'implementazione del server è interamente contenuta nel file [app.py](./app.py).

## Caching
Il sistema di caching è *delegato* al server [`redis`](https://redis.io) e viene utilizzato attraverso la libreria [redis-py](https://github.com/andymccurdy/redis-py).

Una entry in cache rappresenta la qualità dell'aria in un dato giorno a livello nazionale.
L'invalidazione della cache avviene è gestita eliminando i dati più vecchi (quando la cache risulta piena).

Ogni mezz'ora il server si occuperà di aggiornare i dati relativi alla data odierna e ai due giorni precedenti in modo che essi siano sempre disponibili e aggiornati per gli utenti.