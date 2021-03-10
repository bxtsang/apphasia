alter table "public"."project_task_staffs" drop constraint "task_staff_pkey";
alter table "public"."project_task_staffs"
    add constraint "project_task_staffs_pkey" 
    primary key ( "task_id", "staff_id" );
