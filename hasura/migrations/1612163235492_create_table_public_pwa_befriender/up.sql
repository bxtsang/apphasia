CREATE TABLE "public"."pwa_befriender"("pwa_id" integer NOT NULL, "befriender_id" integer NOT NULL, PRIMARY KEY ("pwa_id","befriender_id") , FOREIGN KEY ("pwa_id") REFERENCES "public"."pwa"("id") ON UPDATE restrict ON DELETE cascade, FOREIGN KEY ("befriender_id") REFERENCES "public"."volunteers"("id") ON UPDATE restrict ON DELETE cascade);
