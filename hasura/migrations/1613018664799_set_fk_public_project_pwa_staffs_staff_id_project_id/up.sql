alter table "public"."project_pwa_staffs" drop constraint "project_pwa_staffs_staff_id_fkey",
             add constraint "project_pwa_staffs_staff_id_project_id_fkey"
             foreign key ("staff_id", "project_id")
             references "public"."project_staffs"
             ("staff_id", "project_id") on update restrict on delete cascade;