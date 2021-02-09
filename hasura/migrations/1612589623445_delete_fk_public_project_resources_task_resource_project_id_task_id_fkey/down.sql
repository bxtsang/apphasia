alter table "public"."project_resources" add foreign key ("task_id", "project_id") references "public"."tasks"("id", "project_id") on update restrict on delete cascade;
