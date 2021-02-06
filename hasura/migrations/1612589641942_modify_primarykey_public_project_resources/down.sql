alter table "public"."project_resources" drop constraint "project_resources_pkey";
alter table "public"."project_resources"
    add constraint "task_resource_pkey" 
    primary key ( "task_id", "path", "project_id" );
