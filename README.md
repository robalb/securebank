La reistrazione include un campo password opzionale, e se inserita questa viene salvata nel database
in hash argon2Id. Tuttavia le api non implementano nessun sistema di access control. Ho ritenuto
che un sistema di autenticazione avrebbe interferito troppo con le specifiche richieste, e avrebbe
reso difficile il testing e la valutazione delle api

