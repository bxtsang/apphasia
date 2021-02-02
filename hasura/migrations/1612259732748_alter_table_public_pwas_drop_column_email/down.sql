ALTER TABLE "public"."pwas" ADD COLUMN "email" text;
ALTER TABLE "public"."pwas" ALTER COLUMN "email" DROP NOT NULL;
ALTER TABLE "public"."pwas" ADD CONSTRAINT pwa_email_key UNIQUE (email);
