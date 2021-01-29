alter table "public"."project_staffs" drop constraint "project_staffs_project_id_fkey",
             add constraint "project_staffs_project_id_fkey"
             foreign key ("project_id")
             references "public"."projects"
             ("id") on update restrict on delete cascade;
