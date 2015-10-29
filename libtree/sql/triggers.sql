/* AFTER INSERT */
CREATE OR REPLACE FUNCTION
  update_ancestors_after_insert()
RETURNS TRIGGER AS
$BODY$
BEGIN
  IF NEW.parent IS NOT NULL THEN

    INSERT INTO ancestors
                (node,
                 ancestor)
    SELECT NEW.id,
           ancestor
    FROM   ancestors
    WHERE  node = NEW.parent
    UNION
    SELECT NEW.id,
           NEW.parent;
  END IF;

  RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER update_ancestors_after_insert
AFTER INSERT
ON nodes
FOR EACH ROW
EXECUTE PROCEDURE update_ancestors_after_insert();


/* AFTER DELETE */
CREATE OR REPLACE FUNCTION
  update_ancestors_after_delete()
RETURNS TRIGGER AS
$BODY$
BEGIN

  DELETE FROM nodes AS t1
  USING  ancestors AS t2
  WHERE  t2."ancestor" = OLD.id
         AND t1."id" = t2."node";

  DELETE FROM ancestors AS t1
  USING  ancestors AS t2
  WHERE  t2."ancestor" = OLD.id
         AND t1."node" = t2."node";

  DELETE FROM ancestors AS t1
  USING  ancestors AS t2
  WHERE  t2."ancestor" = OLD.id
         AND t1."ancestor" = t2."node";

  DELETE FROM ancestors
  WHERE  node = OLD.id
          OR ancestor = OLD.id;

  RETURN OLD;

END;
$BODY$
LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER update_ancestors_after_delete
AFTER DELETE
ON nodes
FOR EACH ROW
WHEN (pg_trigger_depth() = 0)
EXECUTE PROCEDURE update_ancestors_after_delete();


/* AFTER UPDATE */
CREATE OR REPLACE FUNCTION
    update_ancestors_after_update()
  RETURNS TRIGGER AS
  $BODY$
  BEGIN

    DELETE FROM ancestors
    WHERE  ancestor IN (SELECT ancestor
                        FROM   ancestors
                        WHERE  node = NEW.id)
           AND node IN (SELECT node
                        FROM   ancestors
                        WHERE  ancestor = NEW.id
                                OR node = NEW.id);

    INSERT INTO ancestors
    SELECT sub.node,
           par.ancestor
    FROM   ancestors AS sub
           JOIN (SELECT ancestor
                 FROM   ancestors
                 WHERE  node = NEW.parent
                 UNION
                 SELECT NEW.parent) AS par
             ON true
    WHERE  sub.ancestor = NEW.id
            OR sub.node = NEW.id;

    IF NEW.parent IS NOT NULL THEN

      INSERT INTO ancestors
                  (node,
                   ancestor)
      SELECT NEW.id,
             ancestor
      FROM   ancestors
      WHERE  node = NEW.parent
      UNION
      SELECT NEW.id,
             NEW.parent;
    END IF;

    RETURN NEW;
  END;
  $BODY$
  LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER update_ancestors_after_update
AFTER UPDATE OF parent
ON nodes
FOR EACH ROW
EXECUTE PROCEDURE update_ancestors_after_update();
