alter table "public"."events"
           add constraint "events_recurr_id_fkey"
           foreign key ("recurr_id")
           references "public"."recurring"
           ("id") on update restrict on delete cascade;
