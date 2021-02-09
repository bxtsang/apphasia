ALTER TABLE "public"."pwas" ADD COLUMN "created_at" timestamptz;
ALTER TABLE "public"."pwas" ALTER COLUMN "created_at" DROP NOT NULL;
ALTER TABLE "public"."pwas" ALTER COLUMN "created_at" SET DEFAULT now();
