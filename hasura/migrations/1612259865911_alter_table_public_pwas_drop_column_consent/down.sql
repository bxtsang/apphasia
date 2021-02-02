ALTER TABLE "public"."pwas" ADD COLUMN "consent" bool;
ALTER TABLE "public"."pwas" ALTER COLUMN "consent" DROP NOT NULL;
