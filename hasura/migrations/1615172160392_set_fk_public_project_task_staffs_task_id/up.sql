alter table "public"."project_task_staffs"
           add constraint "project_task_staffs_task_id_fkey"
           foreign key ("task_id")
           references "public"."project_tasks"
           ("id") on update restrict on delete cascade;
