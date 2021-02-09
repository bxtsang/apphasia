ALTER TABLE "public"."volunteers" ADD COLUMN "date_joined" date;
ALTER TABLE "public"."volunteers" ALTER COLUMN "date_joined" DROP NOT NULL;
ALTER TABLE "public"."volunteers" ALTER COLUMN "date_joined" SET DEFAULT now();
