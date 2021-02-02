ALTER TABLE "public"."pwas" ADD COLUMN "gender" bpchar;
ALTER TABLE "public"."pwas" ALTER COLUMN "gender" DROP NOT NULL;
