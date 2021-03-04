ALTER TABLE "public"."projects" ADD COLUMN "upcoming_datetime" date NOT NULL DEFAULT now();
