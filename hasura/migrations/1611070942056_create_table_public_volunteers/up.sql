CREATE TABLE "public"."volunteers"("id" integer NOT NULL DEFAULT nextval('users_id_seq'::regclass), "email" Text NOT NULL, "name" text NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "nickname" text, "dob" date NOT NULL, "gender" bpchar NOT NULL, "is_active" boolean NOT NULL DEFAULT true, "date_joined" date NOT NULL, "contact_num" integer NOT NULL, "is_speech_therapist" boolean NOT NULL DEFAULT false, "profession" text NOT NULL, "ws_place" text, "nric" text NOT NULL, "bio" text, "type" Text NOT NULL, "status" Integer NOT NULL DEFAULT 0, PRIMARY KEY ("id") , UNIQUE ("email"), UNIQUE ("id"), UNIQUE ("nric"));