ALTER TABLE "public"."staffs" ADD COLUMN "cognito_id" text;
ALTER TABLE "public"."staffs" ALTER COLUMN "cognito_id" DROP NOT NULL;
