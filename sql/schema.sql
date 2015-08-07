CREATE TABLE ancestors
(
  node integer NOT NULL,
  ancestor integer NOT NULL,
  CONSTRAINT idx UNIQUE (node, ancestor)
)
WITH (
  OIDS=FALSE
);

CREATE INDEX idx_ancestor
  ON ancestors
  USING btree
  (ancestor);

CREATE INDEX idx_node
  ON ancestors
  USING btree
  (node);



CREATE TABLE nodes
(
  id serial NOT NULL,
  parent integer,
  type character varying(255),
  "position" smallint DEFAULT NULL,
  attributes jsonb NOT NULL,
  properties jsonb NOT NULL,
  CONSTRAINT "primary" PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

CREATE INDEX idx_parent
  ON nodes
  USING btree
  (parent);
