# Documentazione API
La [specifica](./openapi.yaml) dell'API è stata progettata cercando di seguire il più possibile la specifica **RESTful** ed è inoltre conforme allo standard [Open API](https://github.com/OAI/OpenAPI-Specification/).

Ogni *endpoint* restituisce strutture di tipo `JSON` per cui è opportuno, in fase di richiesta HTTP, impostare l'header `Accept: application/json`.

Data l'origine dei dati (raccolti da varie fonti diverse che hanno tempi di risposta alle volte *biblici*) una richiesta non è immediatamente disponibile almeno che essa non sia stata salvata in *cache*.
Nel caso la richiesta non sia immediatamente disponibile si riceve come risposta un codice **202** (`Accepted`).
È sarà quindi necessario tentare la richiesta alcuni minuti dopo per ricevere la risposta.
Per informazioni sul funzionamento del sistema di *caching* si rimanda alla sezione sulle [scelte implementative]('/ARCHITECTURE.md).

 Endpoint | Metodo | Descrizione                            
 --- | --- | --- 
 [`/api/v1/{anno}/{mese}/{giorno}`](##Qualità-dell'aria-a-livello-nazionale)| GET | Invia la qualità dell'aria a livello nazionale                 
 [`/api/v1/{anno}/{mese}/{giorno}/{regione}`](##Qualità-dell'aria-a-livello-regionale)| GET | Invia la qualità dell'aria a livello regionale
 [`/api/v1/{anno}/{mese}/{giorno}/{regione}/{provincia}`]((##Qualità-dell'aria-a-livello-provinciale)) | GET | Invia la qualità dell'aria a livello provinciale        
 [`/api/v1/dates`]((##Date-disponibili)) | GET | Invia le date disponibili istantaneamente nel sistema
 ---               

## Qualità dell'aria a livello nazionale
`/api/v1/{anno}/{mese}/{giorno}`

### GET
Invia la *QA* (qualità dell'aria) a livello nazionale, regione per regione.

|Nome parametro|Descrizione|Esempio|Posizione|
|---|---|---|---|
`anno`|Rappresenta l'anno di interesse nel formato `YYYY`|`2019`|`path`|
`mese`|Rappresenta il mese di interesse nel formato `MM`|`02`|`path`|
`giorno`|Rappresenta il giorno di interesse nel formato `DD`|`28`|`path`|

 
**Richiesta di esempio**
```bash
curl --header "Accept: application/json" http://<url>/api/v1/2019/01/01`
```

#### Risposte
|Codice|Descrizione|
|---|---|
|200|Risposta OK|
|400|La data che si sta cercando di richiedere è nel futuro|

```json
[
  {
    "href": "http://<url api>/api/v1/2019/1/1/valle%20d%27aosta", 
    "name": "Valle d'Aosta", 
    "provinces": [
      {
        "href": "http://<url api>/api/v1/2019/1/1/valle%20d%27aosta/ao", 
        "name": "Aosta", 
        "quality": {
          "C6H6": 2.2, 
          "CO": 0.8, 
          "NO2": 43.42, 
          "O3": 53.88, 
          "Pm10": 27.8, 
          "Pm2,5": 25.0, 
          "SO2": 12.0
        }, 
        "short": "AO"
      }
    ]
  }, 
  {
    "href": "http://<url api>/api/v1/2019/1/1/piemonte", 
    "name": "Piemonte", 
    "provinces": [
      {
        "href": "http://<url api>/api/v1/2019/1/1/piemonte/al", 
        "name": "Alessandria", 
        "quality": {
          "C6H6": 2.3, 
          "CO": null, 
          "NO2": 52.67, 
          "O3": 35.5, 
          "Pm10": 68.0, 
          "Pm2,5": 49.0, 
          "SO2": 4.0
        }, 
        "short": "AL"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/piemonte/at", 
        "name": "Asti", 
        "quality": {
          "C6H6": 3.3, 
          "CO": 1.3, 
          "NO2": 48.33, 
          "O3": 21.5, 
          "Pm10": null, 
          "Pm2,5": null, 
          "SO2": 8.0
        }, 
        "short": "AT"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/piemonte/bi", 
        "name": "Biella", 
        "quality": {
          "C6H6": 1.65, 
          "CO": 1.0, 
          "NO2": 46.5, 
          "O3": 40.67, 
          "Pm10": 31.0, 
          "Pm2,5": 27.0, 
          "SO2": null
        }, 
        "short": "BI"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/piemonte/cn", 
        "name": "Cuneo", 
        "quality": {
          "C6H6": 1.77, 
          "CO": 0.75, 
          "NO2": 41.33, 
          "O3": 25.25, 
          "Pm10": 51.0, 
          "Pm2,5": 44.0, 
          "SO2": 10.0
        }, 
        "short": "CN"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/piemonte/no", 
        "name": "Novara", 
        "quality": {
          "C6H6": 2.72, 
          "CO": 1.32, 
          "NO2": 47.67, 
          "O3": 34.17, 
          "Pm10": 76.0, 
          "Pm2,5": 69.0, 
          "SO2": 14.5
        }, 
        "short": "NO"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/piemonte/to", 
        "name": "Torino", 
        "quality": {
          "C6H6": 2.29, 
          "CO": 1.1, 
          "NO2": 56.81, 
          "O3": 25.0, 
          "Pm10": 64.0, 
          "Pm2,5": 59.0, 
          "SO2": 13.0
        }, 
        "short": "TO"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/piemonte/vc", 
        "name": "Vercelli", 
        "quality": {
          "C6H6": 1.9, 
          "CO": 0.9, 
          "NO2": 45.75, 
          "O3": 28.5, 
          "Pm10": 59.0, 
          "Pm2,5": 54.0, 
          "SO2": 4.0
        }, 
        "short": "VC"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/piemonte/vb", 
        "name": "Verbano-Cusio-Ossola", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": null, 
          "O3": null, 
          "Pm10": null, 
          "Pm2,5": null, 
          "SO2": null
        }, 
        "short": "VB"
      }
    ]
  }, 
  {
    "href": "http://<url api>/api/v1/2019/1/1/liguria", 
    "name": "Liguria", 
    "provinces": [
      {
        "href": "http://<url api>/api/v1/2019/1/1/liguria/ge", 
        "name": "Genova", 
        "quality": {
          "C6H6": 2.03, 
          "CO": 0.98, 
          "NO2": 60.1, 
          "O3": 17.0, 
          "Pm10": 36.33, 
          "Pm2,5": 30.25, 
          "SO2": 9.17
        }, 
        "short": "GE"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/liguria/im", 
        "name": "Imperia", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": null, 
          "O3": null, 
          "Pm10": null, 
          "Pm2,5": null, 
          "SO2": null
        }, 
        "short": "IM"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/liguria/sp", 
        "name": "La Spezia", 
        "quality": {
          "C6H6": 1.6, 
          "CO": null, 
          "NO2": 72.0, 
          "O3": null, 
          "Pm10": 16.0, 
          "Pm2,5": null, 
          "SO2": null
        }, 
        "short": "SP"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/liguria/sv", 
        "name": "Savona", 
        "quality": {
          "C6H6": 1.99, 
          "CO": 1.0, 
          "NO2": 42.83, 
          "O3": 52.5, 
          "Pm10": 41.83, 
          "Pm2,5": 40.8, 
          "SO2": 5.6
        }, 
        "short": "SV"
      }
    ]
  }, 
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
  }, 
  {
    "href": "http://<url api>/api/v1/2019/1/1/veneto", 
    "name": "Veneto", 
    "provinces": [
      {
        "href": "http://<url api>/api/v1/2019/1/1/veneto/bl", 
        "name": "Belluno", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": 53.5, 
          "O3": 45.67, 
          "Pm10": 23.33, 
          "Pm2,5": null, 
          "SO2": 9.0
        }, 
        "short": "BL"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/veneto/pd", 
        "name": "Padova", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": 62.12, 
          "O3": 9.14, 
          "Pm10": 97.29, 
          "Pm2,5": null, 
          "SO2": 6.75
        }, 
        "short": "PD"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/veneto/ro", 
        "name": "Rovigo", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": 56.5, 
          "O3": 6.0, 
          "Pm10": 64.0, 
          "Pm2,5": null, 
          "SO2": 7.0
        }, 
        "short": "RO"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/veneto/tv", 
        "name": "Treviso", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": 56.6, 
          "O3": 14.0, 
          "Pm10": 58.0, 
          "Pm2,5": null, 
          "SO2": 3.0
        }, 
        "short": "TV"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/veneto/ve", 
        "name": "Venezia", 
        "quality": {
          "C6H6": null, 
          "CO": 2.0, 
          "NO2": 72.71, 
          "O3": 6.6, 
          "Pm10": 81.25, 
          "Pm2,5": null, 
          "SO2": 3.0
        }, 
        "short": "VE"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/veneto/vr", 
        "name": "Verona", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": 62.2, 
          "O3": 31.75, 
          "Pm10": 61.8, 
          "Pm2,5": null, 
          "SO2": 3.0
        }, 
        "short": "VR"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/veneto/vi", 
        "name": "Vicenza", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": 67.0, 
          "O3": 41.0, 
          "Pm10": 62.67, 
          "Pm2,5": null, 
          "SO2": null
        }, 
        "short": "VI"
      }
    ]
  }, 
  {
    "href": "http://<url api>/api/v1/2019/1/1/friuli-venezia%20giulia", 
    "name": "Friuli-Venezia Giulia", 
    "provinces": [
      {
        "href": "http://<url api>/api/v1/2019/1/1/friuli-venezia%20giulia/go", 
        "name": "Gorizia", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": 47.56, 
          "O3": 61.81, 
          "Pm10": 22.1, 
          "Pm2,5": 21.8, 
          "SO2": 3.16
        }, 
        "short": "GO"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/friuli-venezia%20giulia/pn", 
        "name": "Pordenone", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": 42.84, 
          "O3": 48.04, 
          "Pm10": 44.19, 
          "Pm2,5": null, 
          "SO2": null
        }, 
        "short": "PN"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/friuli-venezia%20giulia/ts", 
        "name": "Trieste", 
        "quality": {
          "C6H6": null, 
          "CO": 0.48, 
          "NO2": 58.24, 
          "O3": null, 
          "Pm10": 17.9, 
          "Pm2,5": 12.25, 
          "SO2": 8.1
        }, 
        "short": "TS"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/friuli-venezia%20giulia/ud", 
        "name": "Udine", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": 50.71, 
          "O3": 51.71, 
          "Pm10": 30.02, 
          "Pm2,5": 34.5, 
          "SO2": 0.28
        }, 
        "short": "UD"
      }
    ]
  }, 
  {
    "href": "http://<url api>/api/v1/2019/1/1/trentino%20alto-adige", 
    "name": "Trentino Alto-Adige", 
    "provinces": [
      {
        "href": "http://<url api>/api/v1/2019/1/1/trentino%20alto-adige/tn", 
        "name": "Trento", 
        "quality": {
          "C6H6": null, 
          "CO": 1.04, 
          "NO2": 48.73, 
          "O3": 20.93, 
          "Pm10": 44.38, 
          "Pm2,5": 46.24, 
          "SO2": 3.83
        }, 
        "short": "TN"
      }, 
      {
        "href": "http://<url api>/api/v1/2019/1/1/trentino%20alto-adige/bz", 
        "name": "Bolzano", 
        "quality": {
          "C6H6": null, 
          "CO": null, 
          "NO2": null, 
          "O3": null, 
          "Pm10": null, 
          "Pm2,5": null, 
          "SO2": null
        }, 
        "short": "BZ"
      }
    ]
  }
]
```

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
|400|La data che si sta cercando di richiedere è nel futuro|
|404|La regione specificata non è stata trovata|


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
curl --header "Accept: application/json" http://<url>/api/v1/2019/01/01/lombardia/mi
```

#### Risposte
|Codice|Descrizione|
|---|---|
|200|Richiesta ok|
|400|La data che si sta cercando di richiedere è nel futuro|
|404|La regione oppure la provincia specificata non è stata trovata|

```json
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
}
```

## Date disponibili
`/api/v1/dates`
### GET
Invia le date che attualmente sono disponibili istantaneamente nel sistema.

**Richiesta di esempio**
```bash
curl --header "Accept: application/json" http://<url>/api/v1/dates
```

#### Risposte
|Codice|Descrizione|
|---|---|
|200|Richiesta ok|

```json
[
  "2019-01-01",
  "2019-06-08"
]
```