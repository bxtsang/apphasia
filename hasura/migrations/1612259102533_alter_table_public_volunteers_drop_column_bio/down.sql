ALTER TABLE "public"."volunteers" ADD COLUMN "bio" text;
ALTER TABLE "public"."volunteers" ALTER COLUMN "bio" DROP NOT NULL;
