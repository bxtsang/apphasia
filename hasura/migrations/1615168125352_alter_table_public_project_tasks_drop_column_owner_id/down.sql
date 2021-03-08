ALTER TABLE "public"."project_tasks" ADD COLUMN "owner_id" int4;
ALTER TABLE "public"."project_tasks" ALTER COLUMN "owner_id" DROP NOT NULL;
ALTER TABLE "public"."project_tasks" ADD CONSTRAINT task_owner_id_key UNIQUE (owner_id);
