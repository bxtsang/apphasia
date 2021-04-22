alter table "public"."project_pwa_vols"
           add constraint "project_pwa_vols_pwa_id_fkey"
           foreign key ("pwa_id")
           references "public"."people_external"
           ("id") on update restrict on delete cascade;
