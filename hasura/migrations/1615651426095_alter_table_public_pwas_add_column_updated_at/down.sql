DROP TRIGGER IF EXISTS "set_public_pwas_updated_at" ON "public"."pwas";
ALTER TABLE "public"."pwas" DROP COLUMN "updated_at";
