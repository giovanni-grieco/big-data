DROP TABLE IF EXISTS docs;
CREATE TABLE docs (line STRING);

LOAD DATA INPATH '${hivevar:input_path}' INTO TABLE docs;





DROP TABLE docs;