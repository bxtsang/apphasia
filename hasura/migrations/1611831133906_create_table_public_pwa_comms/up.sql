CREATE TABLE "public"."pwa_comms"("pwa_id" integer NOT NULL, "difficulty" text NOT NULL, PRIMARY KEY ("pwa_id","difficulty") , FOREIGN KEY ("pwa_id") REFERENCES "public"."pwa"("id") ON UPDATE restrict ON DELETE cascade); COMMENT ON TABLE "public"."pwa_comms" IS E'Contains a list of communication difficults of the PWAs';