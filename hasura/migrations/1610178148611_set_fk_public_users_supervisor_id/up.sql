alter table "public"."users"
           add constraint "users_supervisor_id_fkey"
           foreign key ("supervisor_id")
           references "public"."users"
           ("id") on update restrict on delete restrict;
