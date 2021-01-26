ALTER TABLE "public"."volunteers" ADD COLUMN "type" text;
ALTER TABLE "public"."volunteers" ALTER COLUMN "type" DROP NOT NULL;
