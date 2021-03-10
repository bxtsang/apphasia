alter table "public"."project_tasks" drop constraint "task_pkey";
alter table "public"."project_tasks"
    add constraint "project_tasks_pkey" 
    primary key ( "id" );
