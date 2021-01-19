alter table "public"."projects"
           add constraint "projects_owner_id_fkey"
           foreign key ("owner_id")
           references "public"."staffs"
           ("id") on update restrict on delete restrict;
