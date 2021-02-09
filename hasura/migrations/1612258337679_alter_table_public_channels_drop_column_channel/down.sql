ALTER TABLE "public"."channels" ADD COLUMN "channel" text;
ALTER TABLE "public"."channels" ALTER COLUMN "channel" DROP NOT NULL;
