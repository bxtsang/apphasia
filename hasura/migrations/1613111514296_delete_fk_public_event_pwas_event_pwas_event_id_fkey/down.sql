alter table "public"."event_pwas" add foreign key ("event_id") references "public"."events"("id") on update restrict on delete cascade;
