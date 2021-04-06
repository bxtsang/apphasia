alter table "public"."project_pwa_vols" drop constraint "project_pwa_vols_pwa_id_fkey",
          add constraint "project_pwa_vols_project_id_pwa_id_fkey"
          foreign key ("pwa_id", "project_id")
          references "public"."project_pwa"
          ("pwa_id", "project_id")
          on update restrict
          on delete cascade;
