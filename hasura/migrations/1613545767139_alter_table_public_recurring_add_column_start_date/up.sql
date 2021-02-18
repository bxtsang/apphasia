ALTER TABLE "public"."recurring" ADD COLUMN "start_date" date NOT NULL DEFAULT now();
