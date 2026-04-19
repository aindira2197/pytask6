CREATE TABLE ApiData (
  id SERIAL PRIMARY KEY,
  api_name VARCHAR(255) NOT NULL,
  api_url VARCHAR(255) NOT NULL,
  data JSONB NOT NULL
);

CREATE TABLE ApiRequests (
  id SERIAL PRIMARY KEY,
  api_id INTEGER NOT NULL,
  request_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  response_time TIMESTAMP,
  response_code INTEGER,
  response_data JSONB,
  FOREIGN KEY (api_id) REFERENCES ApiData (id)
);

CREATE INDEX idx_ApiRequests_api_id ON ApiRequests (api_id);

CREATE OR REPLACE FUNCTION get_api_data()
RETURNS SETOF ApiData AS $$
DECLARE
  api_row ApiData%ROWTYPE;
BEGIN
  FOR api_row IN SELECT * FROM ApiData LOOP
    RETURN NEXT api_row;
  END LOOP;
  RETURN;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_api_request(id INTEGER)
RETURNS ApiRequests AS $$
DECLARE
  api_request ApiRequests%ROWTYPE;
BEGIN
  SELECT * INTO api_request FROM ApiRequests WHERE id = $1;
  RETURN api_request;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_api_request(api_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
  new_id INTEGER;
BEGIN
  INSERT INTO ApiRequests (api_id) VALUES ($1) RETURNING id INTO new_id;
  RETURN new_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_api_request(id INTEGER, response_code INTEGER, response_data JSONB)
RETURNS VOID AS $$
BEGIN
  UPDATE ApiRequests SET response_code = $2, response_data = $3, response_time = CURRENT_TIMESTAMP WHERE id = $1;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_api_request(id INTEGER)
RETURNS VOID AS $$
BEGIN
  DELETE FROM ApiRequests WHERE id = $1;
END;
$$ LANGUAGE plpgsql;

INSERT INTO ApiData (api_name, api_url) VALUES ('Api1', 'https://api1.com/data');
INSERT INTO ApiData (api_name, api_url) VALUES ('Api2', 'https://api2.com/data');

SELECT * FROM get_api_data();

INSERT INTO ApiRequests (api_id) VALUES (1);
INSERT INTO ApiRequests (api_id) VALUES (2);

SELECT * FROM get_api_request(1);

UPDATE ApiRequests SET response_code = 200, response_data = '{"data": "value"}'::JSONB WHERE id = 1;

SELECT * FROM get_api_request(1);

DELETE FROM ApiRequests WHERE id = 1;

SELECT * FROM get_api_request(1);