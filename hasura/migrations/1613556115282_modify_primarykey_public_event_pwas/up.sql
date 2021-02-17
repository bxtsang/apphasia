alter table "public"."event_pwas" drop constraint "event_pwas_pkey";
alter table "public"."event_pwas"
    add constraint "event_pwas_pkey" 
    primary key ( "pwa_id", "event_id", "project_id" );
