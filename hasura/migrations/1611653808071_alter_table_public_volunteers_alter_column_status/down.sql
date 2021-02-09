ALTER TABLE "public"."volunteers" ALTER COLUMN "status" TYPE integer;
ALTER TABLE ONLY "public"."volunteers" ALTER COLUMN "status" SET DEFAULT '0';
