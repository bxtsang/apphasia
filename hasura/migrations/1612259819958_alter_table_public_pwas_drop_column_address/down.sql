ALTER TABLE "public"."pwas" ADD COLUMN "address" text;
ALTER TABLE "public"."pwas" ALTER COLUMN "address" DROP NOT NULL;
