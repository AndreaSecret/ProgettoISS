# Elyndor: Battle Arena

Elyndor e un videogioco strategico a turni 1vs1 in locale, sviluppato in Python utilizzando la libreria Pygame. Il gioco immerge i giocatori in un mondo fantasy dove due Evocatori si sfidano in battaglie rituali, selezionando e comandando creature magiche note come Mostri del Legame.

Il progetto e stato realizzato come parte del corso di Ingegneria del Software per IA (ISS), seguendo metodologie di sviluppo agili

## Caratteristiche Principali

* **Sistema di Combattimento a Turni:** Gameplay tattico che alterna fasi di attacco e difesa, dove la scelta delle mosse determina l'esito dello scontro.
* **Modalita Draft:** Prima della battaglia, i giocatori selezionano a turno i propri mostri da un pool condiviso. Una scelta strategica iniziale è fondamentale per contrastare l'avversario.
* **Sistema Mosse Plus:** Accumula esperienza durante il combattimento per sbloccare versioni potenziate delle mosse base, aggiungendo effetti secondari come cure, buff o debuff.
* **Roster di Mostri Unici:**
    * **Drago:** Bilanciato e resistente, specializzato in attacchi di fuoco.
    * **Serpe:** Agile e velenosa, con capacita rigenerative, è il più bilanciato fra i tre.
    * **Divoratore:** Un attaccante potente (glass-cannon) con alto attacco ma difese fragili.
* **Grafica Pixel Art:** Stile retro 8-bit con animazioni procedurali fluide per attacchi e transizioni.
* **Architettura Solida:** Codice strutturato secondo il pattern Model-View-Controller (MVC) per garantire manutenibilita ed estendibilita.

## Requisiti di Sistema

Per eseguire il gioco e necessario avere installato sul proprio sistema:

* Python 3.10 o superiore
* Libreria Pygame

## Installazione e Avvio

1.  Clona la repository:
    git clone https://github.com/tuo-username/Elyndor.git
    cd Elyndor

2.  Installa le dipendenze:
    Assicurati di avere pip aggiornato e installa le dipendenze:
    pip install -r requirements.txt

3.  Avvia il gioco:
    Esegui lo script principale dalla root del progetto:
    python run.py

## Comandi di Gioco

Il gioco e interamente controllabile tramite tastiera, progettato per essere accessibile e immediato.

* **Frecce Direzionali:** Navigazione nei menu (Selezione mostri, mosse, opzioni)
* **Invio (Enter):** Conferma selezione / Esegui azione
* **Esc:** Chiudi il gioco 

## Struttura del Progetto

Il codice sorgente e organizzato per separare logicamente le responsabilita:
* **run.py:** Da runnare per far partire il gioco
* **main.py:** Entry point del gioco e game loop principale.
* **game_assets.py:** Contiene la classe Game (Singleton) che gestisce lo stato globale (turni, team, XP).
* **monsters.py:** Definizione delle entita e MonsterFactory per la creazione dei mostri.
* **moves.py:** Logica delle mosse e pattern Decorator per le Mosse Plus.
* **boxes.py & buttons.py:** Gestione dell'interfaccia utente  e rendering delle barre statistiche.
* **animations.py:** Sistema di gestione delle animazioni procedurali (movimenti ellittici e lineari).
* **monster_sprites/:** Cartella contenente gli asset grafici (png) dei mostri.
* **game_files/:** Cartella contenente file strettamente grafici che non sono sprites dei mostri

## Stato dello Sviluppo

Il progetto ha completato la fase di sviluppo principale (Sprint di Gennaio 2026).

Funzionalita Future:
* Implementazione affinita elementali (Fuoco, Acqua, Erba).
* Tutorial interattivo iniziale.
* Log di battaglia testuale a schermo.

## Autori
Alessandro Bombace, Andrea Angelo Segreto, Pietro Sposimo
