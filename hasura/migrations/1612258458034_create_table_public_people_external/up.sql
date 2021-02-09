CREATE TABLE "public"."people_external"("id" serial NOT NULL, "email" Text NOT NULL, "name" text NOT NULL, "date_joined" date NOT NULL DEFAULT now(), "dob" date NOT NULL, "gender" bpchar NOT NULL, "contact_num" integer NOT NULL, "address" text NOT NULL, "notes" text NOT NULL, "bio" text NOT NULL, "consent" boolean NOT NULL, "channel" text NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("channel") REFERENCES "public"."channels"("channel") ON UPDATE cascade ON DELETE restrict, UNIQUE ("email"));
