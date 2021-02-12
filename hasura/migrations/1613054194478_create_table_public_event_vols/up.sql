CREATE TABLE "public"."event_vols"("event_id" integer NOT NULL, "vol_id" integer NOT NULL, PRIMARY KEY ("event_id","vol_id") , FOREIGN KEY ("event_id") REFERENCES "public"."events"("id") ON UPDATE restrict ON DELETE cascade, FOREIGN KEY ("vol_id") REFERENCES "public"."volunteers"("id") ON UPDATE restrict ON DELETE cascade);
