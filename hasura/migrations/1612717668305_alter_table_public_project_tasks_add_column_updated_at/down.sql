DROP TRIGGER IF EXISTS "set_public_project_tasks_updated_at" ON "public"."project_tasks";
ALTER TABLE "public"."project_tasks" DROP COLUMN "updated_at";
