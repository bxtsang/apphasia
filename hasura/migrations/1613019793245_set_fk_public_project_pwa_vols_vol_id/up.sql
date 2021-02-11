alter table "public"."project_pwa_vols" drop constraint "project_pwa_vols_vol_id_project_id_fkey",
             add constraint "project_pwa_vols_vol_id_fkey"
             foreign key ("vol_id")
             references "public"."volunteers"
             ("id") on update restrict on delete cascade;
