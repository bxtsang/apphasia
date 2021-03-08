alter table "public"."project_task_vols" drop constraint "project_task_vols_pkey";
alter table "public"."project_task_vols"
    add constraint "task_vol_pkey" 
    primary key ( "project_id", "task_id", "vol_id" );
