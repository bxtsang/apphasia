ALTER TABLE "public"."people_external" ALTER COLUMN "email" DROP NOT NULL;
ALTER TABLE "public"."people_external" DROP CONSTRAINT "people_external_email_key";
