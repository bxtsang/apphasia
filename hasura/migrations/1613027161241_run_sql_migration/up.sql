CREATE OR REPLACE FUNCTION public.upcoming_date(project_row projects)
 RETURNS date
 LANGUAGE plpgsql
 STABLE
AS $function$
   BEGIN
    RETURN (SELECT date from events WHERE date >= now() and project_id = project_row.id ORDER BY date LIMIT 1);
   END; $function$;
