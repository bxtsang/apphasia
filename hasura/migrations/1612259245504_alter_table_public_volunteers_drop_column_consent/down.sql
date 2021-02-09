ALTER TABLE "public"."volunteers" ADD COLUMN "consent" bool;
ALTER TABLE "public"."volunteers" ALTER COLUMN "consent" DROP NOT NULL;
ALTER TABLE "public"."volunteers" ALTER COLUMN "consent" SET DEFAULT true;
