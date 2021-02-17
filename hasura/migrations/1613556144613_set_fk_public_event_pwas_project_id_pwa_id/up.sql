alter table "public"."event_pwas"
           add constraint "event_pwas_project_id_pwa_id_fkey"
           foreign key ("project_id", "pwa_id")
           references "public"."project_pwa"
           ("project_id", "pwa_id") on update restrict on delete cascade;
