La reistrazione include un campo password opzionale, e se inserita questa viene salvata nel database
in hash argon2Id. Tuttavia le api non implementano nessun sistema di access control. Ho ritenuto
che un sistema di autenticazione avrebbe interferito troppo con le specifiche richieste, e avrebbe
reso difficile il testing e la valutazione delle api


tests:
deve essere possibile

transfer da se stessi a se stessi con valore zero


Queste API implementano in dettaglio le
specifiche fornite nella consegna, con l'unica
differenza nella registrazione, che include un campo password opzionale.

Se inserita, la password opzionale viene salvata nel database
in hash argon2Id. Tuttavia le API non implementano nessun sistema di access control. Ho ritenuto
che un sistema di autenticazione avrebbe interferito troppo con le specifiche richieste, e avrebbe
reso difficile il testing e la valutazione delle api
