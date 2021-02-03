ALTER TABLE "public"."volunteers" ADD COLUMN "email" text;
ALTER TABLE "public"."volunteers" ALTER COLUMN "email" DROP NOT NULL;
ALTER TABLE "public"."volunteers" ADD CONSTRAINT volunteers_email_key UNIQUE (email);
