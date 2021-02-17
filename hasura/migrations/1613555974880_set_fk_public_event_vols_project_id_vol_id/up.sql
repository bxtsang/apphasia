alter table "public"."event_vols"
           add constraint "event_vols_project_id_vol_id_fkey"
           foreign key ("project_id", "vol_id")
           references "public"."project_vol"
           ("project_id", "vol_id") on update restrict on delete cascade;
