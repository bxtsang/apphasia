alter table "public"."event_pwas"
           add constraint "event_pwas_project_id_event_id_fkey"
           foreign key ("project_id", "event_id")
           references "public"."events"
           ("project_id", "id") on update restrict on delete cascade;
