alter table "public"."project_task_vols" drop constraint "task_vol_vol_id_fkey",
             add constraint "project_task_vols_vol_id_project_id_fkey"
             foreign key ("vol_id", "project_id")
             references "public"."project_vol"
             ("vol_id", "project_id") on update restrict on delete cascade;
