alter table "public"."staff_supervisors" drop constraint "staff_supervisors_supervisor_id_fkey",
             add constraint "staff_supervisors_supervisor_id_fkey"
             foreign key ("supervisor_id")
             references "public"."staffs"
             ("id") on update restrict on delete cascade;
