ALTER TABLE "public"."pwas" ADD COLUMN "date_joined" date;
ALTER TABLE "public"."pwas" ALTER COLUMN "date_joined" DROP NOT NULL;
