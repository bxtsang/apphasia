alter table "public"."project_pwa_staffs"
           add constraint "project_pwa_staffs_project_id_fkey"
           foreign key ("project_id")
           references "public"."projects"
           ("id") on update restrict on delete cascade;
