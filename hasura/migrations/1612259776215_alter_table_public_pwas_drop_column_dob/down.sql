ALTER TABLE "public"."pwas" ADD COLUMN "dob" date;
ALTER TABLE "public"."pwas" ALTER COLUMN "dob" DROP NOT NULL;
