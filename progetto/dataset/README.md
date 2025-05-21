# Pipeline di pulizia e porzionamento del dataset

- Puliza del dataset con ```clean_dataset.py```
- Rimozione di colonne inutilizzate con ```drop_columns.py```
- Genera porzioni con ```generate_portions.py```

## Colonne utilizzate
```
name                col  pruned_col
city                7    0
daysonmarket        10   1
description         12   2
engine_displacement 14   3
horsepower          27   4
make_name           42   5
model_name          45   6
price               48   7
year                65   8
```