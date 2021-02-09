ALTER TABLE "public"."pwas" ADD COLUMN "wheelchair" text;
ALTER TABLE "public"."pwas" ALTER COLUMN "wheelchair" DROP NOT NULL;
