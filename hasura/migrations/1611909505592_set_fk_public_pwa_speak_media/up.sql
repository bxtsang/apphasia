alter table "public"."pwa"
           add constraint "pwa_speak_media_fkey"
           foreign key ("speak_media")
           references "public"."answers"
           ("answer") on update cascade on delete restrict;
