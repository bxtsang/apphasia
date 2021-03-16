ALTER TABLE "public"."notifications" ADD COLUMN "created_at" timestamptz NULL DEFAULT now();
