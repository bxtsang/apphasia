alter table "public"."project_tasks" drop constraint "project_tasks_pkey";
alter table "public"."project_tasks"
    add constraint "task_pkey" 
    primary key ( "project_id", "id" );
