alter table "public"."projects"
           add constraint "projects_voltypes_fkey"
           foreign key ("voltypes")
           references "public"."voltypes"
           ("type") on update restrict on delete cascade;
