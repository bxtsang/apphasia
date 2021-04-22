alter table "public"."project_pwa_staffs" drop constraint "project_pwa_staffs_staff_id_fkey2",
             add constraint "project_pwa_staffs_pwa_id_fkey"
             foreign key ("pwa_id")
             references "public"."people_external"
             ("id") on update restrict on delete cascade;
