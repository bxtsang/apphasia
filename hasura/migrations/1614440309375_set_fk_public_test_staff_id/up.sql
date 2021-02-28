alter table "public"."test" drop constraint "test_staff_id_fkey",
             add constraint "test_staff_id_fkey"
             foreign key ("staff_id")
             references "public"."staffs"
             ("id") on update restrict on delete cascade;
