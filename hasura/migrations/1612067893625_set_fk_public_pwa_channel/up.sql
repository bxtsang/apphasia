alter table "public"."pwa"
           add constraint "pwa_channel_fkey"
           foreign key ("channel")
           references "public"."channels"
           ("channel") on update cascade on delete restrict;
