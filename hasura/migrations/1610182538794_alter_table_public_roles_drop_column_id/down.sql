ALTER TABLE "public"."roles" ADD COLUMN "id" int4;
ALTER TABLE "public"."roles" ALTER COLUMN "id" DROP NOT NULL;
ALTER TABLE "public"."roles" ALTER COLUMN "id" SET DEFAULT nextval('roles_id_seq'::regclass);
