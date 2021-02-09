ALTER TABLE "public"."volunteers" ADD COLUMN "contact_num" int4;
ALTER TABLE "public"."volunteers" ALTER COLUMN "contact_num" DROP NOT NULL;
