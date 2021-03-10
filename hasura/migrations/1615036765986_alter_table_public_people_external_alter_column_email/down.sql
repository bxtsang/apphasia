ALTER TABLE "public"."people_external" ALTER COLUMN "email" SET NOT NULL;
ALTER TABLE "public"."people_external" ADD CONSTRAINT "people_external_email_key" UNIQUE ("email");
