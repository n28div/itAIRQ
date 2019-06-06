# Documentazione API
La [specifica](./openapi.yaml) dell'API è stata progettata cercando di seguire il più possibile la specifica **RESTful** ed è inoltre conforme allo standard [Open API](https://github.com/OAI/OpenAPI-Specification/).

Ogni *endpoint* restituisce strutture di tipo `JSON` per cui è opportuno, in fase di richiesta HTTP, impostare l'header `Accept: application/json`.

Le richieste potrebbero impiegare anche alcuni minuti prima di inviare una risposta: questo è dovuto principalmente al tempo richiesto nel ricevere le risposte dagli enti regionali (per maggiori informazioni si veda la sezione sulle [scelte architetturali](./ARCHITECTURE.md)).


 Endpoint | Metodo | Descrizione                            
 --- | --- | --- 
 `/api/v1/{anno}/{mese}/{giorno}`| GET | Invia la qualità media dell'aria a livello nazionale                 
 `/api/v1/{anno}/{mese}/{giorno}/{regione}`| GET | Invia la qualità dell'aria a livello regionale
 `/api/v1/{anno}/{mese}/{giorno}/{regione}/{provincia}` | GET | Invia la qualità dell'aria a livello provinciale        
 ---               

## Qualità dell'aria a livello nazionale
`/api/v1/{anno}/{mese}/{giorno}`

### GET
Invia la *QA* (qualità dell'aria) a livello nazionale, regione per regione.

*QA* viene calcolato effettuando una media dei valori rilevati nelle varie provincie che compongono la funzione

|Nome parametro|Descrizione|Esempio|Posizione|
|---|---|---|---|
`anno`|Rappresenta l'anno di interesse nel formato `YYYY`|`2019`|`path`|
|`mese`|Rappresenta il mese di interesse nel formato `MM`|`02`|`path`|
`giorno`|Rappresenta il giorno di interesse nel formato `DD`|`28`|`path`|

 
**Richiesta di esempio**
```bash
curl --header "Accept: application/json" http://<url>/api/v1/2019/01/01`
```

#### Risposte
|Codice|Descrizione|
|---|---|
|200|Risposta OK|
```json
[
  {
    "C6H6": 2.2, 
    "CO": 0.8, 
    "NO2": 43.42, 
    "O3": 53.88, 
    "Pm10": 27.8, 
    "Pm2,5": 25.0, 
    "SO2": 12.0, 
    "href": "http://<url api>/api/v1/2019/1/1/valle%20d%27aosta", 
    "name": "Valle d'Aosta"
  }, 
  {
    "C6H6": 2.28, 
    "CO": 1.06, 
    "NO2": 48.44, 
    "O3": 30.08, 
    "Pm10": 58.17, 
    "Pm2,5": 50.33, 
    "SO2": 9.0, 
    "href": "http://<url api>/api/v1/2019/1/1/piemonte", 
    "name": "Piemonte"
  }, 
  {
    "C6H6": 1.87, 
    "CO": 0.99, 
    "NO2": 58.31, 
    "O3": 34.75, 
    "Pm10": 31.39, 
    "Pm2,5": 35.52, 
    "SO2": 7.38, 
    "href": "http://<url api>/api/v1/2019/1/1/liguria", 
    "name": "Liguria"
  }, 
  {
    "C6H6": 1.74, 
    "CO": 0.8, 
    "NO2": 71.6, 
    "O3": 11.23, 
    "Pm10": 69.26, 
    "Pm2,5": 58.52, 
    "SO2": 2.44, 
    "href": "http://<url api>/api/v1/2019/1/1/lombardia", 
    "name": "Lombardia"
  }, 
  {
    "C6H6": null, 
    "CO": 2.0, 
    "NO2": 61.52, 
    "O3": 22.02, 
    "Pm10": 64.05, 
    "Pm2,5": null, 
    "SO2": 5.29, 
    "href": "http://<url api>/api/v1/2019/1/1/veneto", 
    "name": "Veneto"
  }
]
```
| | |
|---|---|
|400|La data che si sta cercando di richiedere è nel futuro|



## Qualità dell'aria a livello regionale
`/api/v1/{anno}/{mese}/{giorno}/{regione}`
### GET
Invia la *QA* a livello regionale, provincia per provincia.

|Nome parametro|Descrizione|Esempio|Posizione|
|---|---|---|---|
`anno`|Rappresenta l'anno di interesse nel formato `YYYY`|`2019`|`path`|
|`mese`|Rappresenta il mese di interesse nel formato `MM`|`02`|`path`|
`giorno`|Rappresenta il giorno di interesse nel formato `DD`|`28`|`path`|
|`regione`|Rappresenta la regione di cui si vuol conoscere la qualità dell'aria|`lombardia`|`path`|

**Richiesta di esempio**
```bash
curl --header "Accept: application/json" http://<url>/api/v1/01/01/01/lombardia
```

#### Risposte
|Codice|Descrizione|
|---|---|
|200|Richiesta ok|
```json
{
  "href": "http://<url api>/api/v1/2019/1/1/lombardia", 
  "name": "Lombardia", 
  "provinces": [
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/bg", 
      "name": "Bergamo", 
      "quality": {
        "C6H6": 1.73, 
        "CO": 0.5, 
        "NO2": 65.84, 
        "O3": 6.75, 
        "Pm10": 71.29, 
        "Pm2,5": 60.2, 
        "SO2": 1.46
      }, 
      "short": "BG"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/bs", 
      "name": "Brescia", 
      "quality": {
        "C6H6": 1.9, 
        "CO": 0.54, 
        "NO2": 74.89, 
        "O3": 15.02, 
        "Pm10": 58.8, 
        "Pm2,5": 56.5, 
        "SO2": 1.51
      }, 
      "short": "BS"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/co", 
      "name": "Como", 
      "quality": {
        "C6H6": 1.3, 
        "CO": 0.58, 
        "NO2": 112.43, 
        "O3": 11.7, 
        "Pm10": 66.67, 
        "Pm2,5": 66.0, 
        "SO2": 2.91
      }, 
      "short": "CO"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/cr", 
      "name": "Cremona", 
      "quality": {
        "C6H6": 2.4, 
        "CO": 0.78, 
        "NO2": 64.94, 
        "O3": 6.09, 
        "Pm10": 68.4, 
        "Pm2,5": 52.5, 
        "SO2": 1.76
      }, 
      "short": "CR"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/lc", 
      "name": "Lecco", 
      "quality": {
        "C6H6": 1.1, 
        "CO": 0.77, 
        "NO2": 54.65, 
        "O3": 27.0, 
        "Pm10": 54.4, 
        "Pm2,5": 35.0, 
        "SO2": 1.52
      }, 
      "short": "LC"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/lo", 
      "name": "Lodi", 
      "quality": {
        "C6H6": 1.1, 
        "CO": 0.93, 
        "NO2": 59.42, 
        "O3": 7.72, 
        "Pm10": 69.33, 
        "Pm2,5": 54.5, 
        "SO2": 4.13
      }, 
      "short": "LO"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/mn", 
      "name": "Mantova", 
      "quality": {
        "C6H6": 2.0, 
        "CO": 0.93, 
        "NO2": 61.57, 
        "O3": 8.41, 
        "Pm10": 64.67, 
        "Pm2,5": 56.5, 
        "SO2": 2.08
      }, 
      "short": "MN"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/mi", 
      "name": "Milano", 
      "quality": {
        "C6H6": 2.88, 
        "CO": 1.07, 
        "NO2": 91.31, 
        "O3": 5.89, 
        "Pm10": 93.29, 
        "Pm2,5": 74.33, 
        "SO2": 3.31
      }, 
      "short": "MI"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/mb", 
      "name": "Monza e della Brianza", 
      "quality": {
        "C6H6": null, 
        "CO": 0.84, 
        "NO2": 67.03, 
        "O3": 5.65, 
        "Pm10": 88.0, 
        "Pm2,5": 55.0, 
        "SO2": null
      }, 
      "short": "MB"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/pv", 
      "name": "Pavia", 
      "quality": {
        "C6H6": 1.35, 
        "CO": 0.87, 
        "NO2": 63.15, 
        "O3": 8.77, 
        "Pm10": 72.0, 
        "Pm2,5": 56.67, 
        "SO2": 3.24
      }, 
      "short": "PV"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/so", 
      "name": "Sondrio", 
      "quality": {
        "C6H6": 1.65, 
        "CO": 0.91, 
        "NO2": 74.0, 
        "O3": 20.22, 
        "Pm10": 53.0, 
        "Pm2,5": 65.0, 
        "SO2": 3.32
      }, 
      "short": "SO"
    }, 
    {
      "href": "http://<url api>/api/v1/2019/1/1/lombardia/va", 
      "name": "Varese", 
      "quality": {
        "C6H6": null, 
        "CO": 0.91, 
        "NO2": 69.95, 
        "O3": 11.51, 
        "Pm10": 71.25, 
        "Pm2,5": 70.0, 
        "SO2": 1.63
      }, 
      "short": "VA"
    }
  ]
}
```
| | |
|---|---|
|400|La data che si sta cercando di richiedere è nel futuro|
|404|La regione specificata non è stata trovata|

## Qualità dell'aria a livello provinciale
`/api/v1/{anno}/{mese}/{giorno}/{regione}/{provincia}`
### GET
Invia la *QA* di una provincia.

|Nome parametro|Descrizione|Esempio|Posizione|
|---|---|---|---|
`anno`|Rappresenta l'anno di interesse nel formato `YYYY`|`2019`|`path`|
|`mese`|Rappresenta il mese di interesse nel formato `MM`|`02`|`path`|
`giorno`|Rappresenta il giorno di interesse nel formato `DD`|`28`|`path`|
|`regione`|Rappresenta la regione in cui si trova la provincia|`lombardia`|`path`|
|`provincia`|Rappresenta la provincia di cui si vuol conoscere la qualità dell'aria|`mi` oppure `milano`|`path`|


**Richiesta di esempio**
```bash
curl --header "Accept: application/json" http://<url>/api/v1/01/01/01/lombardia/mi
```

#### Risposte
|Codice|Descrizione|
|---|---|
|200|Richiesta ok|
```json
{
  "href": "http://127.0.0.1:5000/api/v1/2019/1/1/lombardia/mi", 
  "name": "Milano", 
  "quality": {
    "C6H6": 2.88, 
    "CO": 1.07, 
    "NO2": 91.31, 
    "O3": 5.89, 
    "Pm10": 93.29, 
    "Pm2,5": 74.33, 
    "SO2": 3.31
  }, 
  "short": "MI"
}
```
| | |
|---|---|
|400|La data che si sta cercando di richiedere è nel futuro|
|404|La regione oppure la provincia specificata non è stata trovata|
