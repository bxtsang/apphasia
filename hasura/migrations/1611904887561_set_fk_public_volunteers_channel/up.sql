alter table "public"."volunteers" drop constraint "volunteers_channel_fkey",
             add constraint "volunteers_channel_fkey"
             foreign key ("channel")
             references "public"."channels"
             ("channel") on update cascade on delete restrict;
