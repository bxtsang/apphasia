alter table "public"."pwas"
           add constraint "pwas_contact_status_fkey"
           foreign key ("contact_status")
           references "public"."pwa_contact_status"
           ("status") on update cascade on delete restrict;
