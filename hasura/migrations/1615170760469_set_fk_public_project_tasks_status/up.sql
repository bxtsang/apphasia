alter table "public"."project_tasks"
           add constraint "project_tasks_status_fkey"
           foreign key ("status")
           references "public"."project_task_status"
           ("status") on update restrict on delete restrict;
