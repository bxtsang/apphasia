ALTER TABLE "public"."staffs" ADD COLUMN "nric" text;
ALTER TABLE "public"."staffs" ALTER COLUMN "nric" DROP NOT NULL;
