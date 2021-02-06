CREATE TABLE "public"."task_vol"("project_id" integer NOT NULL, "task_id" integer NOT NULL, "vol_id" integer NOT NULL, PRIMARY KEY ("project_id","task_id","vol_id") , FOREIGN KEY ("vol_id") REFERENCES "public"."volunteers"("id") ON UPDATE restrict ON DELETE cascade, FOREIGN KEY ("task_id", "project_id") REFERENCES "public"."tasks"("id", "project_id") ON UPDATE restrict ON DELETE cascade);