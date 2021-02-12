CREATE TABLE "public"."event_pwas"("event_id" integer NOT NULL, "pwa_id" integer NOT NULL, PRIMARY KEY ("event_id","pwa_id") , FOREIGN KEY ("event_id") REFERENCES "public"."events"("id") ON UPDATE restrict ON DELETE cascade, FOREIGN KEY ("pwa_id") REFERENCES "public"."pwas"("id") ON UPDATE restrict ON DELETE cascade);