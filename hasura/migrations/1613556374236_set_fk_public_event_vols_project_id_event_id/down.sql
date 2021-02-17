alter table "public"."event_vols" drop constraint "event_vols_project_id_event_id_fkey",
          add constraint "event_vols_project_id_vol_id_fkey"
          foreign key ("vol_id", "project_id")
          references "public"."project_vol"
          ("vol_id", "project_id")
          on update restrict
          on delete cascade;
