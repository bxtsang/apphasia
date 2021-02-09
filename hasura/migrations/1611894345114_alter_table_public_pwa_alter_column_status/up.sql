ALTER TABLE ONLY "public"."pwa" ALTER COLUMN "status" SET DEFAULT 'Not Contacted';
ALTER TABLE "public"."pwa" ALTER COLUMN "status" SET NOT NULL;
