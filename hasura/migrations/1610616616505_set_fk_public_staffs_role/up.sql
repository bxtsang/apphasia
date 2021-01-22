alter table "public"."staffs"
           add constraint "staffs_role_fkey"
           foreign key ("role")
           references "public"."roles"
           ("role") on update restrict on delete restrict;
