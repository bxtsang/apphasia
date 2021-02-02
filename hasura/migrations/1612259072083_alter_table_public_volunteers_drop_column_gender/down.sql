ALTER TABLE "public"."volunteers" ADD COLUMN "gender" bpchar;
ALTER TABLE "public"."volunteers" ALTER COLUMN "gender" DROP NOT NULL;
