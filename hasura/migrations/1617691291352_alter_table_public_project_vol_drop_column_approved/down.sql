ALTER TABLE "public"."project_vol" ADD COLUMN "approved" bool;
ALTER TABLE "public"."project_vol" ALTER COLUMN "approved" DROP NOT NULL;
ALTER TABLE "public"."project_vol" ALTER COLUMN "approved" SET DEFAULT false;
