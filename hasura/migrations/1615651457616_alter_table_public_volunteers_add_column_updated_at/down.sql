DROP TRIGGER IF EXISTS "set_public_volunteers_updated_at" ON "public"."volunteers";
ALTER TABLE "public"."volunteers" DROP COLUMN "updated_at";
