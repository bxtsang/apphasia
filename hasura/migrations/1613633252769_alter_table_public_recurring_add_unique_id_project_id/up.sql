alter table "public"."recurring" add constraint "recurring_id_project_id_key" unique ("id", "project_id");
