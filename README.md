# Laptop E-commerce
Laptop E-commerce è un progetto web sviluppato con Django, che consente agli utenti di comprare e vendere laptop.

Il sito offre anche funzioni come la ricerca, con la possibilità di inserire diversi parametri come nome del laptop, il brand del processore, la ram, lo storage e un budget massimo, e l'inserimento da parte deqli acquirenti di recensioni sia per i laptop che per i fornitori.

## Requisiti
- Python 3.12
- Django 5.1.2
- virtual environment

## Installazione
### Clona il repository ed entra nella cartella top-level di progetto
```
git clone https://github.com/karim1655/Laptop_ecommerce.git

cd Laptop_ecommerce
```
### Installa pipenv
```
pip install pipenv
```
### Crea ambiente virtuale
```
pipenv install
```
Questo comando creerà un nuovo ambiente virtuale e installerà tutte le dipendenze elencate nel file Pipfile (se presente). Altrimenti pipenv creerà un ambiente vuoto.
### Attiva ambiente virtuale
```
pipenv install
```
### Installa le dipendenze
```
pipenv install -r requirements.txt
```
### Esegui le migrazioni per il database
```
python manage.py migrate
```
### Crea il superutente per accedere alla console admin (facoltativo)
```
python manage.py createsuperuser
```
### Avvia il server di sviluppo
```
python manage.py runserver
```
### Accedi
Inserisci http://localhost:8000 in un qualunque browser per accedere all'applicazione.

## Utilizzo
Il database è già popolato con alcune istanze sia di acquirenti che di fornitori.
La password è sempre: `bellabro1`

Acquirenti:
- Michael
- Dwight
- Jim
- Pam

Fornitori:
- Apple
- HP
- Lenovo

## Testing
Per eseguire i test:
```
python manage.py test
```


