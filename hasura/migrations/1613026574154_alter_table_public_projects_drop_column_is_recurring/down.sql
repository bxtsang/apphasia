ALTER TABLE "public"."projects" ADD COLUMN "is_recurring" bool;
ALTER TABLE "public"."projects" ALTER COLUMN "is_recurring" DROP NOT NULL;
ALTER TABLE "public"."projects" ALTER COLUMN "is_recurring" SET DEFAULT false;
