CREATE TRIGGER `collection_garbage_collector` AFTER DELETE ON `user_has_collection`
 FOR EACH ROW BEGIN

DECLARE refs integer;

SET @refs := (SELECT COUNT(collection_id) FROM user_has_collection WHERE collection_id = OLD.collection_id);

IF(@refs <= 0)
THEN
	DELETE FROM collection WHERE collection_id = OLD.collection_id;
END IF;

END

CREATE TRIGGER `document_garbage_collector` AFTER DELETE ON `collection_has_document`
 FOR EACH ROW BEGIN

DECLARE refs integer;

SET @refs := (SELECT COUNT(document_id) FROM collection_has_document WHERE document_id = OLD.document_id);

IF(@refs <= 0)
THEN
	DELETE FROM document WHERE document_id = OLD.document_id;
END IF;

END

CREATE TRIGGER `user_prepare_private_coll` BEFORE INSERT ON `user`
 FOR EACH ROW BEGIN

DECLARE coll_id integer;