# Task 1 - Hive

In questo task viene chiesto di raggruppare per modello tutte le auto del dataset.


Per ciascun modello, la casa produttrice, il costo medio, massimo e minimo, quante volte appare il modello all'interno del dataset e gli in cui è esistito nel dataset.

```
manufacturer  model   amount  min_prica   max_price   avg_price   years

Aston Martin  Rapide  1       89668.0     89668.0     89668.0     {2016}
Audi          S7      3       26942.0     59999.0     41146.7	  {2016, 2014, 2015}
```

## Esecuzione esperimenti

Gli esperimenti possono essere effettuati utilizzando lo script ```run_experiment.py```.
```bash
# È diverso dall'esecuzione di esperimenti spark-core e mapreduce, qui non c'è distinzione tra remote e local
python3 run_experiment.py results.csv
```
