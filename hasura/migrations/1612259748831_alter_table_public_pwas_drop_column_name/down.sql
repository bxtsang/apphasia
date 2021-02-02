ALTER TABLE "public"."pwas" ADD COLUMN "name" text;
ALTER TABLE "public"."pwas" ALTER COLUMN "name" DROP NOT NULL;
