ALTER TABLE "public"."projects" ADD COLUMN "is_active" text;
ALTER TABLE "public"."projects" ALTER COLUMN "is_active" DROP NOT NULL;
ALTER TABLE "public"."projects" ALTER COLUMN "is_active" SET DEFAULT 'true'::text;
