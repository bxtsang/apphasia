alter table "public"."event_vols"
           add constraint "event_vols_project_id_event_id_fkey"
           foreign key ("project_id", "event_id")
           references "public"."events"
           ("project_id", "id") on update restrict on delete cascade;
