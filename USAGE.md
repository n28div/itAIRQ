# Utilizzo della webapp
## Installare i requisiti
```bash
pip install -r requirements.txt
```

## Avvio del server
Per il testing del server è necessario modificare la variabile `debug` in [settings.py](./settings.py) con `debug = TRUE`.

Per avviare il server è quindi sufficiente il comando
```bash
python app.py
```

Per l'utilizzo in produzione di consiglia di consultare la sezione [deploy](./DEPLOY.md).
