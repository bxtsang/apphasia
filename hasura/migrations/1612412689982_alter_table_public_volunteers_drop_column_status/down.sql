ALTER TABLE "public"."volunteers" ADD COLUMN "status" text;
ALTER TABLE "public"."volunteers" ALTER COLUMN "status" DROP NOT NULL;
ALTER TABLE "public"."volunteers" ALTER COLUMN "status" SET DEFAULT 'Pending_Approval'::text;
