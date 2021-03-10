ALTER TABLE "public"."project_task_staffs" ADD COLUMN "project_id" int4;
ALTER TABLE "public"."project_task_staffs" ALTER COLUMN "project_id" DROP NOT NULL;
ALTER TABLE "public"."project_task_staffs" ADD CONSTRAINT project_task_staffs_staff_id_project_id_fkey FOREIGN KEY (project_id, staff_id) REFERENCES "public"."project_staffs" (project_id, staff_id) ON DELETE cascade ON UPDATE restrict;
ALTER TABLE "public"."project_task_staffs" ADD CONSTRAINT task_staff_task_id_project_id_fkey FOREIGN KEY (project_id, task_id) REFERENCES "public"."project_tasks" (project_id, id) ON DELETE cascade ON UPDATE restrict;
