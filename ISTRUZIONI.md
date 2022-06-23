# istruzioni per l'installazione

prerequisiti: Docker e Docker-compose.
é sufficente installare [Docker desktop](https://docs.docker.com/get-docker/)
per ottenerli.

Testato su windows 10 e ubuntu 22, usando le ultime versioni stabili di Docker e Docker-compose

- con il vostro terminale, navigate nella cartella principale del progetto,
  quella contenente questo file ISTRUZIONI che state leggendo.
- eseguite il comando `docker-compose up --build`

Verranno creati tre servizi:

- http://localhost:5000/ un webserver Nginx che serve il sito
- http://localhost:8080/ il server delle api
- locahost:3306 il database mariadb


## Info utili

La documentazione open api interattiva è situata all'indirizzo
http://localhost:8080/docs 
Questa pagina elenca gli endpoint esistenti e le loro specifiche, e permette
di testarli in tempo reale tramite un' interfaccia web.

Per accedere al database, usare le credenziali salvate nel file `.env`, ovvero
user: test password: test

## Disinstallazione

- con il vostro terminale, navigate nella cartella principale del progetto,
  quella contenente questo file ISTRUZIONI che state leggendo.
- eseguite `docker-compose down -v`


