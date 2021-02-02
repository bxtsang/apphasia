ALTER TABLE "public"."pwas" ADD COLUMN "channel" text;
ALTER TABLE "public"."pwas" ALTER COLUMN "channel" DROP NOT NULL;
