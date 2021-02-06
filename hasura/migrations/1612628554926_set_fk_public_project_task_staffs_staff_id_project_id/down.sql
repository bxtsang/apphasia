alter table "public"."project_task_staffs" drop constraint "project_task_staffs_staff_id_project_id_fkey",
          add constraint "task_staff_staff_id_fkey"
          foreign key ("staff_id")
          references "public"."staffs"
          ("id")
          on update restrict
          on delete cascade;
