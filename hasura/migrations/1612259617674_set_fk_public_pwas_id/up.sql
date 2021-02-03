alter table "public"."pwas"
           add constraint "pwas_id_fkey"
           foreign key ("id")
           references "public"."people_external"
           ("id") on update restrict on delete restrict;
