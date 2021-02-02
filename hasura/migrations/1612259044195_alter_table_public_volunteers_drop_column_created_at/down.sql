ALTER TABLE "public"."volunteers" ADD COLUMN "created_at" timestamptz;
ALTER TABLE "public"."volunteers" ALTER COLUMN "created_at" DROP NOT NULL;
ALTER TABLE "public"."volunteers" ALTER COLUMN "created_at" SET DEFAULT now();
