alter table "public"."test"
           add constraint "test_staff_id_fkey"
           foreign key ("staff_id")
           references "public"."staffs"
           ("id") on update restrict on delete restrict;
