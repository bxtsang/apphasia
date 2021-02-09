ALTER TABLE "public"."volunteers" ADD COLUMN "notes" text;
ALTER TABLE "public"."volunteers" ALTER COLUMN "notes" DROP NOT NULL;
