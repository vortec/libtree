CREATE TABLE ancestor
(
  node integer NOT NULL,
  ancestor integer NOT NULL,
  CONSTRAINT idx UNIQUE (node, ancestor)
)
WITH (
  OIDS=FALSE
);

CREATE INDEX idx_ancestor
  ON ancestor
  USING btree
  (ancestor);

CREATE INDEX idx_node
  ON ancestor
  USING btree
  (node);



CREATE TABLE nodes
(
  id serial NOT NULL,
  parent integer,
  type character varying(255),
  "position" smallint DEFAULT NULL,
  CONSTRAINT "primary" PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

CREATE INDEX idx_parent
  ON nodes
  USING btree
  (parent);
