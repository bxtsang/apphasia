ALTER TABLE "public"."staffs" ADD COLUMN "languages" int4;
ALTER TABLE "public"."staffs" ALTER COLUMN "languages" DROP NOT NULL;
