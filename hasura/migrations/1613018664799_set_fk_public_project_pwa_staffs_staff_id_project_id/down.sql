alter table "public"."project_pwa_staffs" drop constraint "project_pwa_staffs_staff_id_project_id_fkey",
          add constraint "project_pwa_staffs_staff_id_fkey"
          foreign key ("staff_id")
          references "public"."staffs"
          ("id")
          on update restrict
          on delete cascade;
