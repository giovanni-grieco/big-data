SET hive.exec.mode.local.auto=false;
SET mapreduce.map.memory.mb=4096;
SET mapreduce.reduce.memory.mb=4096;
SET mapreduce.map.java.opts=-Xmx4g;
SET mapreduce.reduce.java.opts=-Xmx4g;
SET hive.groupby.skewindata=true;
SET hive.exec.parallel=true;

-- 1. Crea la tabella cars se non esiste, con tutte le colonne del CSV
DROP TABLE IF EXISTS cars;
CREATE TABLE cars (
    city STRING, 
    daysonmarket INT,
    description STRING,
    engine_displacement FLOAT,
    horsepower FLOAT,
    make_name STRING,
    model_name STRING,
    price FLOAT,
    year INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '${hivevar:input_path}' OVERWRITE INTO TABLE cars;

-- 2. Crea tabella con la colonna fascia_prezzo
CREATE TABLE IF NOT EXISTS cars_with_fascia AS
SELECT *,
  CASE
    WHEN price > 50000 THEN 'alta'
    WHEN price BETWEEN 20000 AND 50000 THEN 'media'
    ELSE 'bassa'
  END AS fascia_prezzo
FROM cars;

-- 3. Statistiche per città, anno, fascia
CREATE TABLE IF NOT EXISTS stat_fascia_prezzo AS
SELECT city, year, fascia_prezzo,
  COUNT(*) AS num_cars,
  AVG(daysonmarket) AS avg_daysonmarket
FROM cars_with_fascia
GROUP BY city, year, fascia_prezzo;

-- 4. Frequenza parole
CREATE TABLE IF NOT EXISTS word_freq AS
SELECT city, year, fascia_prezzo, word, COUNT(*) AS freq
FROM cars_with_fascia
LATERAL VIEW EXPLODE(SPLIT(description, '\\s+')) exploded_words AS word
GROUP BY city, year, fascia_prezzo, word;

-- 5. Top 3 parole
CREATE TABLE IF NOT EXISTS top_words AS
SELECT city, year, fascia_prezzo, word, freq
FROM (
  SELECT city, year, fascia_prezzo, word, freq,
    ROW_NUMBER() OVER (PARTITION BY city, year, fascia_prezzo ORDER BY freq DESC) AS rn
  FROM word_freq
) ranked
WHERE rn <= 3;

-- 6. Creazione tabella finale con i risultati grezzi
CREATE TABLE IF NOT EXISTS report_cars AS
SELECT
  s.city,
  s.year,
  s.fascia_prezzo,
  s.num_cars,
  s.avg_daysonmarket,
  CONCAT_WS(', ',
    MAX(CASE WHEN t.freq_rank = 1 THEN t.word END),
    MAX(CASE WHEN t.freq_rank = 2 THEN t.word END),
    MAX(CASE WHEN t.freq_rank = 3 THEN t.word END)
  ) AS top_3_words
FROM stat_fascia_prezzo s
LEFT JOIN (
  SELECT city, year, fascia_prezzo, word, freq,
    ROW_NUMBER() OVER (PARTITION BY city, year, fascia_prezzo ORDER BY freq DESC) AS freq_rank
  FROM top_words
) t
  ON s.city = t.city AND s.year = t.year AND s.fascia_prezzo = t.fascia_prezzo
GROUP BY s.city, s.year, s.fascia_prezzo, s.num_cars, s.avg_daysonmarket;

-- 7. (Facoltativo) Visualizza risultati grezzi
SELECT * FROM report_cars;
