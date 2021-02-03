ALTER TABLE ONLY "public"."volunteers" ALTER COLUMN "id" SET DEFAULT nextval('volunteers_id_seq'::regclass);
