ALTER TABLE "public"."projects" ADD COLUMN "upcoming_datetime" date;
ALTER TABLE "public"."projects" ALTER COLUMN "upcoming_datetime" DROP NOT NULL;
ALTER TABLE "public"."projects" ALTER COLUMN "upcoming_datetime" SET DEFAULT now();
