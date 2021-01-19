ALTER TABLE "public"."staffs" ADD COLUMN "supervisor_id" int4;
ALTER TABLE "public"."staffs" ALTER COLUMN "supervisor_id" DROP NOT NULL;
