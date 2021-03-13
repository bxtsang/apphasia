DROP TRIGGER IF EXISTS "set_public_staffs_updated_at" ON "public"."staffs";
ALTER TABLE "public"."staffs" DROP COLUMN "updated_at";
