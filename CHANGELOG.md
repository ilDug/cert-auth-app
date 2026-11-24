# Changelog

## Unreleased

Modifiche incluse dopo `5fad520`:

### Aggiunto
- Registrati i dati locali italiani nell'applicazione.

### Migliorato
- Aggiornata la gestione di certificati e chiavi, passando a risorse reattive per il caricamento e l'aggiornamento dei dati.
- Rifattorizzato il dialogo di creazione dei certificati per usare Signal Forms, con validazione e messaggi d'errore più chiari.
- Migliorata la visualizzazione degli errori nella lista dei certificati.

### Corretto
- Gestita la data di revoca nulla nei certificati.
- Corretto il reset della PKI, passando la configurazione alla funzione di installazione.

### Manutenzione
- Rimossa la classe legacy `Certificate` e riordinati gli export del frontend.
- Aggiornate la configurazione del proxy frontend e le schermate di certificati e chiavi per il nuovo modello di risorse.
