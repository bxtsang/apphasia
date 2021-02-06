alter table "public"."project_resources"
           add constraint "project_resources_project_id_fkey"
           foreign key ("project_id")
           references "public"."projects"
           ("id") on update restrict on delete cascade;
