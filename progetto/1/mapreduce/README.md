# Task 1 - MapReduce

In questo task viene chiesto di raggruppare per modello tutte le auto del dataset.


Per ciascun modello, la casa produttrice, il costo medio, massimo e minimo, quante volte appare il modello all'interno del dataset e gli in cui è esistito nel dataset.

```
manufacturer  model   amount  min_prica   max_price   avg_price   years_range

Toyota        ECHO    1       3599.0      3599.0      3599.0      1
Volkswagen    Tiguan  170     5550.0      41464.0     25134.1     11
```

## Mapper

## Descrizione del Mapper e Reducer

### Mapper

Il mapper elabora i dati relativi alle auto usate dal dataset CSV, estraendo le seguenti informazioni per ogni riga:

- Produttore (manufacturer)
- Modello (model)
- Prezzo (price)
- Anno (year)

Il mapper legge ogni riga in input, divide i campi separati da virgole e seleziona solo le colonne rilevanti. L'output viene emesso nel formato:

```
manufacturer\tmodel\tprice\tyear
```

Il mapper gestisce anche le potenziali eccezioni durante l'elaborazione, scrivendo i messaggi di errore nello stderr.

### Reducer

Il reducer prende in input i dati emessi dal mapper e li aggrega per modello di auto. Per ogni modello, calcola:

1. Produttore dell'auto
2. Numero totale di occorrenze nel dataset (amount)
3. Prezzo minimo (min_price)
4. Prezzo massimo (max_price)
5. Prezzo medio (avg_price)
6. Intervallo di anni in cui il modello appare nel dataset (years_range)

Il reducer calcola queste statistiche mantenendo varie strutture dati per tracciare le informazioni necessarie durante l'elaborazione. L'output finale viene formattato come:

```
manufacturer\tmodel\tcount\tmin_price\tmax_price\tavg_price\tyears_range
```

Questo output presenta un riepilogo completo delle statistiche per ogni modello di auto presente nel dataset.