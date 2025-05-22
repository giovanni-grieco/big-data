# Pipeline di pulizia e porzionamento del dataset

- Puliza del dataset con ```clean_dataset.py```
- Rimozione di colonne inutilizzate con ```drop_columns.py```
- Genera porzioni con ```generate_portions.py```

## Colonne utilizzate
```
type     name                col  pruned_col
string   city                7    0
int      daysonmarket        10   1
string   description         12   2
float    engine_displacement 14   3
float    horsepower          27   4
string   make_name           42   5
string   model_name          45   6
float(?) price               48   7
int      year                65   8
```