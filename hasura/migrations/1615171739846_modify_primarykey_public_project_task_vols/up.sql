alter table "public"."project_task_vols" drop constraint "task_vol_pkey";
alter table "public"."project_task_vols"
    add constraint "project_task_vols_pkey" 
    primary key ( "task_id", "vol_id" );
