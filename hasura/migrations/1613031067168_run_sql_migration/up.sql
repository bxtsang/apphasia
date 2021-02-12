CREATE TRIGGER update_events_values_trigger
  AFTER UPDATE
  ON recurring
  FOR EACH ROW
  EXECUTE PROCEDURE update_events_values();
