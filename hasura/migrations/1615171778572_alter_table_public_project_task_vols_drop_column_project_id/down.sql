ALTER TABLE "public"."project_task_vols" ADD COLUMN "project_id" int4;
ALTER TABLE "public"."project_task_vols" ALTER COLUMN "project_id" DROP NOT NULL;
ALTER TABLE "public"."project_task_vols" ADD CONSTRAINT project_task_vols_vol_id_project_id_fkey FOREIGN KEY (vol_id, project_id) REFERENCES "public"."project_vol" (vol_id, project_id) ON DELETE cascade ON UPDATE restrict;
ALTER TABLE "public"."project_task_vols" ADD CONSTRAINT task_vol_task_id_project_id_fkey FOREIGN KEY (project_id, task_id) REFERENCES "public"."project_tasks" (project_id, id) ON DELETE cascade ON UPDATE restrict;
