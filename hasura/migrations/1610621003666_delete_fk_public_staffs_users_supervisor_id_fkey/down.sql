alter table "public"."staffs" add foreign key ("supervisor_id") references "public"."staffs"("id") on update restrict on delete restrict;
