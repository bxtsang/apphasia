ALTER TABLE "public"."users" ADD COLUMN "role_id" int4;
ALTER TABLE "public"."users" ALTER COLUMN "role_id" DROP NOT NULL;
ALTER TABLE "public"."users" ALTER COLUMN "role_id" SET DEFAULT nextval('users_type_id_seq'::regclass);
