alter table "public"."events" add constraint "events_id_project_id_key" unique ("id", "project_id");
