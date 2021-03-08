ALTER TABLE "public"."project_tasks" ADD COLUMN "updated_at" timestamptz;
ALTER TABLE "public"."project_tasks" ALTER COLUMN "updated_at" DROP NOT NULL;
ALTER TABLE "public"."project_tasks" ALTER COLUMN "updated_at" SET DEFAULT now();
