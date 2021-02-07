ALTER TABLE "public"."project_tasks" ADD COLUMN "created_at" timestamptz;
ALTER TABLE "public"."project_tasks" ALTER COLUMN "created_at" DROP NOT NULL;
ALTER TABLE "public"."project_tasks" ALTER COLUMN "created_at" SET DEFAULT now();
