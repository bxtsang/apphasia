alter table "public"."staff_supervisors" drop constraint "supervisor_staff";
alter table "public"."staff_supervisors" add constraint "supervisor_staff" check (staff_id <> supervisor_id);
