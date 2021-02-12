alter table "public"."event_pwas" drop constraint "event_pwas_project_id_pwa_id_fkey",
          add constraint "event_pwas_pwa_id_fkey"
          foreign key ("pwa_id")
          references "public"."pwas"
          ("id")
          on update restrict
          on delete cascade;
