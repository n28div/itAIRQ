# Valle d'aosta
[http://www.arpa.vda.it/it/aria/la-qualit%C3%A0-dell-aria/stazioni-di-monitoraggio/dati-e-grafici]

* `SO2`
* `NO2`
* `CO`
* `O3`
* `Pm10`
* `Pm2.5`
* `C6H6`

# Piemonte
[http://www.sistemapiemonte.it/ambiente/srqa/consultadati.shtml?tipo=S&parametro=05&dd=05&mm=02&yyyy=2019]

* `C6H6`
* `CO`
* `NO2`
* `NO`
* `PTS`
* `O3`
* `Pm10`
* `Pm2.5`
* `SO2`

# Lombardia
[https://www.dati.lombardia.it/Ambiente/Dati-sensori-aria/nicp-bhqi]
[https://www.dati.lombardia.it/Ambiente/Stazioni-qualit-dell-aria/ib47-atvt]

* `Biossido di Zolfo`
* `Monossido di Carbonio`
* `Ossidi di Azoto`
* `Biossido di Azoto`
* `Benzene`
* `Ozono`
* `Nikel`
* `Cadmio`
* `Particelle sospese PM2.5`
* `Benzo(a)pirene`
* `PM10 (SM2005)`
* `Particolato Totale Sospeso`
* `Piombo`
* `Ammoniaca`
* `Arsenico`
* `PM10`
* `BlackCarbon`

# Veneto
[http://www.arpa.veneto.it/arpavinforma/bollettini/aria/aria_dati_validati.php?provincia=Belluno]
[http://www.arpa.veneto.it/arpavinforma/bollettini/aria/aria_dati_validati.php?provincia=Padova]
[http://www.arpa.veneto.it/arpavinforma/bollettini/aria/aria_dati_validati.php?provincia=Rovigo]
[http://www.arpa.veneto.it/arpavinforma/bollettini/aria/aria_dati_validati.php?provincia=Treviso]
[http://www.arpa.veneto.it/arpavinforma/bollettini/aria/aria_dati_validati.php?provincia=Venezia]
[http://www.arpa.veneto.it/arpavinforma/bollettini/aria/aria_dati_validati.php?provincia=Verona]
[http://www.arpa.veneto.it/arpavinforma/bollettini/aria/aria_dati_validati.php?provincia=Vicenza]

* `NO2`
* `Pm10`
* `O3`
* `SO2`
* `CO`

# Friuli Venezia-Giulia
[https://www.dati.friuliveneziagiulia.it/browse?q=Aria&sortBy=relevance]

* `Pm10`
* `Ozono`
* `Monossido di carbonio`
* `Biossido d'Azoto`
* `Biossido di Zolfo`
* `Pm2.5`

# Liguria
[http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub3AccessoDatiAria.asp?Tipo=DatiGiorno]

* `Benzene`
* `Biossido di Azoto`
* `Biossido di Zolfo`
* `Monossido di Carbonio`
* `Ozono`
* `Pm10`
* `Pm2,5`

# Emilia-Romagna
[https://apps.arpae.it/qualita-aria/bollettino-qa/20190501]

* `NO2`
* `O3`
* `Benzene`
* `CO`
* `SO2`
* `Pm10`
* `Pm2,5`

# Toscana
[http://www.arpat.toscana.it/temi-ambientali/aria/qualita-aria/bollettini/bollettino_json/regionale/16-05-2019]

* `NO2`
* `H2S`
* `Benzene`
* `CO`
* `SO2`
* `Pm10`
* `Pm2,5`

# Marche
```
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'Connection': 'keep-alive',
}

data = {
  'ctl00$MainContent5$ScriptManager1': 'ctl00$MainContent5$pnlReportLoading|ctl00$MainContent5$ddlProv',
  'ctl00$MainContent5$ddlProv': 'All',
  'ctl00$MainContent5$txtReportDate': '19/05/2019',
  '__EVENTTARGET': 'ctl00$MainContent5$ddlProv',
  '__VIEWSTATE': '/wEPDwUJLTk2Mjc4Nzg2D2QWAmYPZBYCAgMPZBYCAg8PZBYCAgEPZBYCZg9kFhYCAw8PFgIeB1Zpc2libGVoZGQCBw8QZBAVBw5TZWxlemlvbmFyZS4uLhNQcm92aW5jaWEgZGkgQW5jb25hGlByb3ZpbmNpYSBkaSBBc2NvbGkgUGljZW5vElByb3ZpbmNpYSBkaSBGZXJtbxVQcm92aW5jaWEgZGkgTWFjZXJhdGEcUHJvdmluY2lhIGRpIFBlc2FybyBlIFVyYmlubxFUdXR0ZSBsZSBwcm92aW5jZRUHBG51bGwCQU4CQVACRk0CTUMCUFUDQWxsFCsDB2dnZ2dnZ2cWAQIBZAIJDw9kFgIeC29ubW91c2VvdmVyBRp0aGlzLnN0eWxlLmN1cnNvciA9ICdoZWxwJ2QCDw9kFggCAQ8PFgIfAGdkZAIDDw8WAh8AZ2RkAgUPDxYEHgRUZXh0BQZBbmNvbmEfAGdkZAIHDw8WBB8CBQoxOS8wNS8yMDE5HwBnZGQCEQ8PFgIfAGdkZAITDw8WAh8AZ2RkAhUPDxYCHwBnZGQCFw8PFgIfAGdkZAIZDw8WAh8AaGRkAhsPZBYkAgEPDxYCHwBnZGQCAw8PFgIfAGdkFgJmD2QWAgIEDw8WAh8CBS1NZWRpYSBhbm51YWxlIHByb2dyZXNzaXZhICjCtWcvbTxzdXA+Mzwvc3VwPilkZAIFDw8WAh8AZ2QWAmYPZBYCAgcPDxYCHwIFLU1lZGlhIGFubnVhbGUgcHJvZ3Jlc3NpdmEgKMK1Zy9tPHN1cD4zPC9zdXA+KWRkAgcPDxYCHwBnZGQCCQ8PFgIfAGdkZAILDw8WAh8AZ2RkAg0PDxYCHwBnZGQCDw8PFgIfAGdkZAIRDw8WAh8AZ2RkAhMPDxYCHwBnZGQCFQ8PFgIfAGdkZAIXDw8WAh8AZ2RkAhkPDxYCHwBnZGQCGw8PFgIfAGhkZAIdDw8WAh8AaGRkAh8PDxYCHwBoZGQCIQ8PFgIfAGhkZAIjDw8WAh8AaGRkAh0PDxYCHwBnZGQYAQUUY3RsMDAkTmF2aWdhdGlvbk1lbnUPD2QFCVJpZXBpbG9nb2S25FJX2rblbNVoraSPEo1UewPiP4Efg36kVd4qKAIWaA==',
  '__VIEWSTATEGENERATOR': '1C8BD2A4',
  '__EVENTVALIDATION': '/wEdAAwqKKPHeOl005twhT9aX8MifPFElMDidsmezAt0I1LbonikRt4uq2V3KEjoubSfTzThEI9mYQUosF9vUs734PPO8G/n4CGqv51sqgaUJOI7fAq52L7mFEtFo79dvzFY2L/cOj89tZ6IOxa3qJlxG/tDEYTuHw/QXcT0bIfQOJFRW0Ii2jN4X4TD44bJE6CJmgAqy3dq+LlS163TkFWVyLk+TgsAVUkkCpeRi6r4WSUZeFpibD9iH7OcvxIYMwvqCxR9cgZgH7Ix46PE6EVhhQoKpwCNkWt6WTuY6ho58RvUkg==',
}

response = requests.post('http://94.88.42.232:16382/Report.aspx', headers=headers, cookies=cookies, data=data)
```

* `NO2`
* `O3`
* `CO`
* `SO2`
* `Pm10`
* `Pm2,5`
* `C6H6`

# Umbria
[http://www.arpa.umbria.it/monitoraggi/aria/Default.aspx]

* `NO2`
* `O3`
* `CO`
* `SO2`
* `Pm10`
* `Pm2,5`

# Abruzzo
[https://sira.artaabruzzo.it/server/20190513.json?updates={"param":"data","value":"2019-5-13","op":"s"}]

* `NO2`
* `O3`
* `CO`
* `SO2`
* `Pm10`
* `Pm2,5`
* `C6H6`

# Lazio
[http://www.arpalazio.net/main/aria/sci/qa/misure/NO2.php]

* `NO2`
* `NOX`
* `CO`
* `SO2`
* `Pm10`
* `Pm2,5`
* `C6H6`
* `O3`


# Molise
[http://www.arpamoliseairquality.it/stazioni/]

* `NO2`
* `CO`
* `SO2`
* `Pm10`

# Puglia
[http://arpa.puglia.it/pentaho/ViewAction?solution=ARPAPUGLIA&path=metacatalogo&action=meta-aria.xaction]
[http://arpa.puglia.it/web/guest/qaria?p_p_id=QAriaFilterPortlet_WAR_pentaho&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_pos=3&p_p_col_count=6&PROVINCIA=&INQUINANTE=&DATA=20190515&=&=2019]

* `BLACK CARB`
* `C6H6`
* `CO`
* `H2S`
* `IPA TOT`
* `NO2`
* `O3`
* `PM10`
* `PM2.5`
* `SO2`

# Campania
[http://www.arpacampania.it/web/guest/55]

* `NO2`
* `CO`
* `SO2`
* `Pm10`
* `Pm2.5`
* `O3`
* `Benzene`

# Basilicata
[http://www.arpab.it/aria/qa.asp?giorno=02%2F05%2F2019]

* `NO2`
* `CO`
* `SO2`
* `Pm10`
* `Pm2.5`
* `Ozono`
* `Benzene`
* `H2S`
* `NMHC`

# Calabria
[http://2.228.94.230/web/guest/bollettino-generale]

* `NO2`
* `CO`
* `SO2`
* `Pm10`
* `Pm2.5`
* `O3`
* `Benzene`

# Sicilia
[https://www.arpa.sicilia.it/temi-ambientali/aria/bollettino-aria/?dt=16/5/2019]

* `NO2`
* `CO`
* `SO2`
* `Pm10`
* `Pm2.5`
* `O3`
* `Benzene`

# Sardegna
[https://portal.sardegnasira.it/ricerca-centraline]
un bel casino **PD**

* `NO2`
* `CO`
* `SO2`
* `Pm10`
* `Pm2.5`
* `O3`
* `Benzene`



