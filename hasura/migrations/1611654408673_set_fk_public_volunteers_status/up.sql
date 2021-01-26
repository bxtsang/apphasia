alter table "public"."volunteers"
           add constraint "volunteers_status_fkey"
           foreign key ("status")
           references "public"."status"
           ("status") on update restrict on delete restrict;
