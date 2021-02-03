ALTER TABLE "public"."volunteers" ADD COLUMN "address" text;
ALTER TABLE "public"."volunteers" ALTER COLUMN "address" DROP NOT NULL;
