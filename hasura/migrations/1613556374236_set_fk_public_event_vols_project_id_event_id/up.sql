alter table "public"."event_vols" drop constraint "event_vols_project_id_vol_id_fkey",
             add constraint "event_vols_project_id_event_id_fkey"
             foreign key ("project_id", "event_id")
             references "public"."events"
             ("project_id", "id") on update restrict on delete cascade;
