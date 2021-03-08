alter table "public"."project_task_staffs" drop constraint "project_task_staffs_pkey";
alter table "public"."project_task_staffs"
    add constraint "task_staff_pkey" 
    primary key ( "task_id", "staff_id", "project_id" );
