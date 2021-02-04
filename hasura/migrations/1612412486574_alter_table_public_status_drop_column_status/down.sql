ALTER TABLE "public"."status" ADD COLUMN "status" text;
ALTER TABLE "public"."status" ALTER COLUMN "status" DROP NOT NULL;
