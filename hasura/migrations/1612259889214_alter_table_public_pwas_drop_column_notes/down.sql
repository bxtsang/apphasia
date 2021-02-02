ALTER TABLE "public"."pwas" ADD COLUMN "notes" text;
ALTER TABLE "public"."pwas" ALTER COLUMN "notes" DROP NOT NULL;
