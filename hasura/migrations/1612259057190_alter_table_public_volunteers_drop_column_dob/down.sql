ALTER TABLE "public"."volunteers" ADD COLUMN "dob" date;
ALTER TABLE "public"."volunteers" ALTER COLUMN "dob" DROP NOT NULL;
