alter table "public"."project_resources" drop constraint "task_resource_pkey";
alter table "public"."project_resources"
    add constraint "project_resources_pkey" 
    primary key ( "path", "project_id" );
