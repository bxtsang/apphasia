alter table "public"."vol_channels"
           add constraint "vol_channels_channels_fkey"
           foreign key ("channels")
           references "public"."channels"
           ("channel") on update restrict on delete restrict;
