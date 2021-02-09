ALTER TABLE "public"."volunteers" ADD COLUMN "name" text;
ALTER TABLE "public"."volunteers" ALTER COLUMN "name" DROP NOT NULL;
