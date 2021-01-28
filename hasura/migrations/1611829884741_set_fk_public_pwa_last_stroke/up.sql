alter table "public"."pwa"
           add constraint "pwa_last_stroke_fkey"
           foreign key ("last_stroke")
           references "public"."last_stroke"
           ("when") on update restrict on delete restrict;
