CREATE TABLE "public"."vol_supervisors"("vol_id" integer NOT NULL, "staff_id" integer NOT NULL, PRIMARY KEY ("vol_id","staff_id") , FOREIGN KEY ("vol_id") REFERENCES "public"."volunteers"("id") ON UPDATE restrict ON DELETE cascade, FOREIGN KEY ("staff_id") REFERENCES "public"."staffs"("id") ON UPDATE restrict ON DELETE cascade);
