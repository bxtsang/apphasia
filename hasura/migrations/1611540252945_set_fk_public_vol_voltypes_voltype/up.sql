alter table "public"."vol_voltypes"
           add constraint "vol_voltypes_voltype_fkey"
           foreign key ("voltype")
           references "public"."voltypes"
           ("type") on update restrict on delete restrict;
