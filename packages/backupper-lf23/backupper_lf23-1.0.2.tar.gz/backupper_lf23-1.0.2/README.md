# Backupper

Backupper è uno strumento Python per la gestione dei backup in formato ZIP o TAR

## Installazione

Per installare Backupper, usa pip:

``` bash
pip install backupper
```
## Funzionalità

- Creazione di archivi ZIP e TAR.
- Estrazione di archivi compressi ZIP o TAR.
- Cancellazione di archivi, partendo dal meno recente.
- Supporto per archivi solo ZIP protetti da password.

## Utilizzo
```
Crea un backup della directory corrente in formato ZIP (default):
backupper -c .
	
Crea un backup della directory corrente in formato TAR:
backupper -c -f tar .

Estrai un archivio dalla directory corrente con nome corrispondente alla directory corrente e data più recente:
backupper -x .

Cancella un archivio specificando il formato tar, con nome directory corrente:
backupper -d -f tar .
```
## Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file LICENSE per maggiori dettagli.
