CREATE OR REPLACE FUNCTION public.upcoming_project_date(project_row projects)
 RETURNS timestamp with time zone
 LANGUAGE plpgsql
 STABLE
AS $function$
   BEGIN
    RETURN (WITH updated AS (SELECT project_id,GENERATE_SERIES(date, now() + '1 years'::INTERVAL, 
            CASE recurring_schedule 
            WHEN 'Weekly' 
                THEN '1 weeks'::INTERVAL
            WHEN 'Bi-Weekly'
                THEN '2 weeks'::INTERVAL
            WHEN 'Monthly'
                THEN '1 month'::INTERVAL
            ELSE '999 years'::INTERVAL
            END) as rc
        FROM project_dates ORDER BY rc) 
        SELECT rc FROM updated
        WHERE (rc >= now() AND project_row.id = project_id) LIMIT 1);
   END; $function$;
