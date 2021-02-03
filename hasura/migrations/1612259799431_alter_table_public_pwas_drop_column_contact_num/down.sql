ALTER TABLE "public"."pwas" ADD COLUMN "contact_num" int4;
ALTER TABLE "public"."pwas" ALTER COLUMN "contact_num" DROP NOT NULL;
