alter table "public"."event_vols" add foreign key ("event_id") references "public"."events"("id") on update restrict on delete cascade;
