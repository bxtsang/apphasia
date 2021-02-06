CREATE TABLE "public"."project_dates"("project_id" integer NOT NULL, "date" timestamptz NOT NULL, "recurring_schedule" text, PRIMARY KEY ("project_id","date") , FOREIGN KEY ("project_id") REFERENCES "public"."projects"("id") ON UPDATE restrict ON DELETE cascade);