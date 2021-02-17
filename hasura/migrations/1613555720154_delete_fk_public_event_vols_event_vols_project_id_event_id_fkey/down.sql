alter table "public"."event_vols" add foreign key ("project_id", "event_id") references "public"."events"("project_id", "id") on update restrict on delete cascade;
