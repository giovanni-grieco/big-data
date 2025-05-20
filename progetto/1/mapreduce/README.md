# Task 1 - MapReduce

In questo task viene chiesto di raggruppare per modello tutte le auto del dataset.


Per ciascun modello, la casa produttrice, il costo medio, massimo e minimo, quante volte appare il modello all'interno del dataset e gli in cui è esistito nel dataset.

```
manufacturer  model   amount  min_prica   max_price   avg_price   years

Aston Martin  Rapide  1       89668.0     89668.0     89668.0     {2016}
Audi          S7      3       26942.0     59999.0     41146.7	  {2016, 2014, 2015}
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
6. Un insieme ordinato di anni in cui il modello appare nel dataset (years)

Il reducer calcola queste statistiche mantenendo varie strutture dati per tracciare le informazioni necessarie durante l'elaborazione. L'output finale viene formattato come:

```
manufacturer\tmodel\tcount\tmin_price\tmax_price\tavg_price\t{year1,year2,...yearN}
```

Questo output presenta un riepilogo completo delle statistiche per ogni modello di auto presente nel dataset.