ALTER TABLE "public"."project_resources" ADD COLUMN "task_id" int4;
ALTER TABLE "public"."project_resources" ALTER COLUMN "task_id" DROP NOT NULL;
