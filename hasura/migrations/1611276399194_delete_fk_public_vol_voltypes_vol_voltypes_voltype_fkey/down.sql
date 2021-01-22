alter table "public"."vol_voltypes" add foreign key ("voltype") references "public"."voltypes"("type") on update restrict on delete restrict;
