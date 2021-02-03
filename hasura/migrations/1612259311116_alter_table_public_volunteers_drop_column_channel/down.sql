ALTER TABLE "public"."volunteers" ADD COLUMN "channel" text;
ALTER TABLE "public"."volunteers" ALTER COLUMN "channel" DROP NOT NULL;
