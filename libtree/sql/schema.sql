CREATE TABLE ancestors
  (
     node     INTEGER NOT NULL,
     ancestor INTEGER NOT NULL,
     CONSTRAINT idx UNIQUE (node, ancestor)
  ) with ( oids=FALSE );

CREATE INDEX idx_ancestor ON ancestors USING btree (ancestor);

CREATE INDEX idx_node ON ancestors USING btree (node);

CREATE TABLE nodes
  (
     id         SERIAL NOT NULL,
     parent     INTEGER,
     "position" SMALLINT DEFAULT NULL,
     properties JSONB NOT NULL,
     CONSTRAINT "primary" PRIMARY KEY (id)
  ) with ( oids=FALSE );

CREATE INDEX idx_parent ON nodes USING btree (parent);
