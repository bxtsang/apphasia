CREATE OR REPLACE FUNCTION update_events_values()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
AS $function$
DECLARE
    days text;
    weeks text;
BEGIN
    
    IF NEW.name <> OLD.name THEN
         UPDATE events SET name = NEW.name WHERE recurr_id = NEW.id;
    END IF;
    IF NEW.note <> OLD.note THEN
         UPDATE events SET note = NEW.note WHERE recurr_id = NEW.id;
    END IF;
    IF NEW.start_time <> OLD.start_time THEN
        UPDATE events SET start_time = NEW.start_time WHERE recurr_id = NEW.id;
    END IF;
    IF NEW.end_time <> OLD.end_time THEN
        UPDATE events SET end_time = NEW.end_time WHERE recurr_id = NEW.id;
    END IF;
    IF NEW.end_date < OLD.end_date THEN
        DELETE FROM events WHERE date >= NEW.end_date AND recurr_id = NEW.id;
    END IF;
    IF NEW.day <> OLD.day THEN
        days := (NEW.day - OLD.day)::text || ' day';
        UPDATE events t1 SET date = x.myDate FROM (
        SELECT id, (date + days::interval) as myDate FROM events WHERE recurr_id = NEW.id) x
        WHERE t1.id = x.id;
    END IF;
    IF NEW.week <> OLD.week THEN
        weeks := (NEW.week - OLD.week)::text || ' weeks';
        UPDATE events t1 SET date = x.myDate FROM (
        SELECT id, (date + weeks::interval) as myDate FROM events WHERE recurr_id = NEW.id) x
        WHERE t1.id = x.id;
    END IF;
    RETURN NEW;
END;
$function$;
