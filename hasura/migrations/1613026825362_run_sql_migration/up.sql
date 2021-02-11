CREATE OR REPLACE FUNCTION public.is_recurring(project_row projects)
 RETURNS boolean
 LANGUAGE plpgsql
 STABLE
AS $function$
    DECLARE
    total_events integer;
   BEGIN
    SELECT COUNT(id) into total_events FROM events WHERE project_id = project_row.id;
    IF total_events > 1 THEN RETURN TRUE;
    ELSE RETURN FALSE;
    END IF;
   END; $function$;
