ALTER TABLE "public"."volunteers" ADD COLUMN "nric" text;
ALTER TABLE "public"."volunteers" ALTER COLUMN "nric" DROP NOT NULL;
ALTER TABLE "public"."volunteers" ADD CONSTRAINT volunteers_nric_key UNIQUE (nric);
