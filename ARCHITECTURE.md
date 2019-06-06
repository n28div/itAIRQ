# Architettura adottata
L'API è stata scritta utilizzando il linguaggio *Python* e si divide in due *"macro-componenti"* differenti:
 * [I componenti che si occupano di scaricare i dati dai vari siti delle regioni](#scaricamento-dei-dati)
 * Il componente che si occupa di aggregare tutti i dati di tutte le regioni e fornirli tramite l'API RESTful

## Scaricamento dei dati
Lo scaricamento dei dati viene effettuato diversamente per ogni regione poiché ogni regione fornisce diversamente i propri dati.

Per far si che l'API possa lavorare con un interfaccia omogenea ogni regione è una classe derivata da [`BaseRegion`](regions/region.py).

L'implementazione di una regione consiste nell'overriding del metodo costruttore (`__init__`) in cui vengono registrate le province di una regione e nell'overriding del metodo `_fetch_air_quality_routine` in cui viene implementata la routine di scaricamento e manipolazione dei dati presi dalle varie regioni. Esso viene effettuato su un thread separato così da poter effettuare lo scaricamento di più regioni in parallelo.

Le librerie utilizzate in questa fase sono:
 * [requests](https://3.python-requests.org/) utilizzata per effettuare richieste HTTP
 * [BeutifulSoup 4](https://www.crummy.com/software/BeautifulSoup/) utilizzata per lo scraping delle pagine HTML nel caso esso fosse necessario
 * [html-table-extractor](https://github.com/yuanxu-li/html-table-extractor) per effettuare una gestione a più alto livello delle tabelle HTML
 * [sodapy](https://github.com/xmunoz/sodapy) utilizzato per le regioni che offrono i propri dati come Open Data utilizzando [Socrata](https://www.tylertech.com/products/socrata)
