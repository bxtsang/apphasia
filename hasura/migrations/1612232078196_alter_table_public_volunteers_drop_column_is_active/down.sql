ALTER TABLE "public"."volunteers" ADD COLUMN "is_active" bool;
ALTER TABLE "public"."volunteers" ALTER COLUMN "is_active" DROP NOT NULL;
ALTER TABLE "public"."volunteers" ALTER COLUMN "is_active" SET DEFAULT true;
