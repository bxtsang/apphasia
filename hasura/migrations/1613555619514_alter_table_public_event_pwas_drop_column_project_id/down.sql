ALTER TABLE "public"."event_pwas" ADD COLUMN "project_id" int4;
ALTER TABLE "public"."event_pwas" ALTER COLUMN "project_id" DROP NOT NULL;
ALTER TABLE "public"."event_pwas" ADD CONSTRAINT event_pwas_project_id_pwa_id_fkey FOREIGN KEY (project_id, pwa_id) REFERENCES "public"."project_pwa" (project_id, pwa_id) ON DELETE cascade ON UPDATE restrict;
ALTER TABLE "public"."event_pwas" ADD CONSTRAINT event_pwas_project_id_event_id_fkey FOREIGN KEY (event_id, project_id) REFERENCES "public"."events" (id, project_id) ON DELETE cascade ON UPDATE restrict;
