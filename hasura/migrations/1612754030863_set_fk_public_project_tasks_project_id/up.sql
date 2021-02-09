alter table "public"."project_tasks"
           add constraint "project_tasks_project_id_fkey"
           foreign key ("project_id")
           references "public"."projects"
           ("id") on update restrict on delete cascade;
