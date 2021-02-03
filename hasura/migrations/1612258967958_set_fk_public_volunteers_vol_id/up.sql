alter table "public"."volunteers"
           add constraint "volunteers_vol_id_fkey"
           foreign key ("vol_id")
           references "public"."people_external"
           ("id") on update restrict on delete restrict;
