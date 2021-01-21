ALTER TABLE "public"."users" ADD COLUMN "role" text;
ALTER TABLE "public"."users" ALTER COLUMN "role" DROP NOT NULL;
ALTER TABLE "public"."users" ADD CONSTRAINT users_role_fkey FOREIGN KEY (role) REFERENCES "public"."roles" (role) ON DELETE restrict ON UPDATE restrict;
