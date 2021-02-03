ALTER TABLE "public"."pwas" ADD COLUMN "hobbies" text;
ALTER TABLE "public"."pwas" ALTER COLUMN "hobbies" DROP NOT NULL;
