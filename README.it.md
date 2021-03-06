# Info

Autore: Alberto Ventafridda 866135

Repository del progetto: https://github.com/robalb/securebank


# Installazione

vedere il file [ ISTRUZIONI.md ]( ./ISTRUZIONI.md )



# descrizione del progetto

### architettura

L'architetttura del progetto si può riassumere nei tre seguenti elementi:

- **web**: framework Svelte.js, con vite.js come bundler e Nginx come server di produzione
- **api**: Python, con il framework fastAPI
- **database**: Mariadb, modellato usando SQLWorkbench

Questi tre elementi sono associati a tre rispettive immagini Docker
che possono essere utilizate tramite i file docker-compose forniti oppure,
con le opportune modifiche, tramite kubernetes. Questa consegna non tratta
il tema kubernetes, per quello vedere la repository completa del progetto
https://github.com/robalb/securebank

### api

> http://localhost:8080/

Le API implementano in dettaglio le
specifiche fornite nella consegna, senza endpoint aggiuntivi o sostanziali
modifiche.

Una documentazione dettagliata e interattiva delle api è disponibile all'indirizzo
http://localhost:8080/docs (è necessario lanciare prima il progetto seguendo le 
[istruzioni](./ISTRUZIONI.md).)
Questa pagina elenca gli endpoint esistenti e le loro specifiche, e permette
di testarli in tempo reale tramite un' interfaccia web.

In alternativa la stessa documentazione è disponibile in formato OpenAPI nel seguente
file json [openapi.json](./openapi.json)

La registrazione include un campo password opzionale, e se inserita questa viene salvata nel database
in hash argon2Id. Tuttavia le api non implementano nessun sistema di access control. Ho ritenuto
che un sistema di autenticazione avrebbe interferito troppo con le specifiche richieste, e avrebbe
reso difficile il testing e la valutazione delle api



### web

> http://localhost:5000/

Il frontend è stato realizzato usando il framework Svelte,
 che offre (come tutti i framework javascript moderni)
un sistema reattivo e la possibilità di organizzare il prorio sistema in componenti.
Il vantaggio di svelte sta nel fatto che il framework non complica l'interazione
diretta con il DOM, facilitando addiruttura l'uso di api come
[Constraint validation api](https://developer.mozilla.org/en-US/docs/Web/API/Constraint_validation) o
[Intl](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl).

Il risultato è stato un sistema accessibile, facilmente internazionalizzabile,
che raggiunge un punteggio di 100/100 in fatto di accessibilità e best practices
su google lighthouse.

Per lo stile del sito ho usato bootstrap con il seguente tema vintage:

    WIN95.CSS
    https://github.com/AlexBSoft/win95.css
    Author: Alex B (alex-b.me)
    License: MIT

Il tema consiste in un singolo file css, che ho lievemente modificato per essere
 piu accessibile e incluso tra i miei assets in `/web/src/assets`

Sempre tra gli asset statici ho incluso alcune icone e il file css di bootstrap,
per evitare di dipendere da un CDN.

### database

> localhost:3306 user:test password: test

Per accedere al database, usare le credenziali salvate nel file `.env`, ovvero
user: test password: test


# sviluppo in locale

> **Note**
> Questa sezione elenca le istruzioni per lo sviluppo in locale del progetto.
> Tutto quello che segue non è rilevante per la valutazione del progetto.

ci sono tre aree principali di sviluppo: web, api, e database.
Quelle che seguono sono le istruzioni per lo sviluppo di ciascuna area.

### sviluppo web

- con il vostro terminale, navigare in `/web`
- installare le dipendenze `npm install`
- lanciare il devserver `npm run dev`

eseguendo questi passaggi il sito web in modalità sviluppo sarà
disponibile all'indirizzo http://localhost:3000/

Modifiche apportate ai file contenuti in `/web/src` faranno automaticamente aggiornare
la pagina web del sito in sviluppo.

In modalità sviluppo, il sito è configurato per comunicare alle api situate
all'indirizzo http://localhost:8080/api

Per lanciare le api, vedi la sezione seguente:

### sviluppo api

- con il vostro terminale, navigate nella cartella principale del progetto,
  quella contenente questo README che state leggendo.
- eseguite `docker-compose -f docker-compose.dev.yml up --build`
 
eseguendo questi passaggi le api in modalità sviluppo saranno disponibili
all'indirizzo http://localhost:8080/

e la documentazione interattiva delle api sarà disponibile all'indirizzo
http://localhost:8080/docs
Da qui è possibile testare ed eseguire chiamate a tutti gli endpoint delle api

Modifiche apportate ai file contenuti in `/api/app` faranno automaticamente
aggiornare il server api e la documentazione interattiva.

Il database utilizzato da fastapi si trova in ascolto sulla porta 3306,
ed è possibile connettercisi utilizzando le credenziali definite nel file `.env`
situato nella cartella principale del progetto. Di default sono user:test password:test

Per apportare modifiche al database, vedi la sezione seguente:

### sviluppo database

Il database utilizzato è stato modellato usando lo strumento grafico
MYSQLWorkbench. Il file del progetto si trova in `/dbmodel/sql-models.mwb`

Una volta apportate modifiche al modello, lo si può esportare in un file sql

Il file sql esportato va modificato per essere compatibile con
mariadb seguendo le istruzioni in
(/dbmodel/workbench-export-instructions)[/dbmodel/workbench-export-instructions.md]

