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
STORED AS TEXTFILE;

LOAD DATA INPATH '${hivevar:input_path}' OVERWRITE INTO TABLE used_cars;


SELECT make_name as manufacturer, model_name as model, AVG(price) as avg_price, MIN(price) as min_price, MAX(price) as max_price, COUNT(*) as count
FROM used_cars
GROUP BY make_name, model_name
ORDER BY make_name, model_name; 



DROP TABLE used_cars;