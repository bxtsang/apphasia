ALTER TABLE "public"."project_vol" ADD COLUMN "interested" bool;
ALTER TABLE "public"."project_vol" ALTER COLUMN "interested" DROP NOT NULL;
ALTER TABLE "public"."project_vol" ALTER COLUMN "interested" SET DEFAULT true;
