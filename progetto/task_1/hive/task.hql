DROP TABLE IF EXISTS used_cars;

CREATE TABLE used_cars (
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

LOAD DATA INPATH '${hivevar:input_path}' OVERWRITE INTO TABLE used_cars;


SELECT 
    make_name AS manufacturer, 
    model_name AS model, 
    COUNT(*) AS count,
    AVG(price) AS avg_price, 
    MIN(price) AS min_price, 
    MAX(price) AS max_price, 
    COLLECT_SET(CAST(year AS STRING)) AS years_str
FROM used_cars
GROUP BY make_name, model_name
ORDER BY make_name, model_name;

DROP TABLE IF EXISTS used_cars;