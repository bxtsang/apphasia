alter table "public"."volunteers"
           add constraint "volunteers_channel_fkey"
           foreign key ("channel")
           references "public"."channels"
           ("channel") on update restrict on delete restrict;
