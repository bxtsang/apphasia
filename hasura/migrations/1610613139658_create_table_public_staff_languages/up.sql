CREATE TABLE "public"."staff_languages"("staff_id" integer NOT NULL, "language" text NOT NULL, PRIMARY KEY ("staff_id","language") , FOREIGN KEY ("staff_id") REFERENCES "public"."users"("id") ON UPDATE restrict ON DELETE cascade, FOREIGN KEY ("language") REFERENCES "public"."languages"("language") ON UPDATE restrict ON DELETE restrict);
