alter table "public"."pwa"
           add constraint "pwa_wheelchair_fkey"
           foreign key ("wheelchair")
           references "public"."answers"
           ("answer") on update restrict on delete restrict;
