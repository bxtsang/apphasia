alter table "public"."event_vols" drop constraint "event_vols_vol_id_project_id_fkey",
          add constraint "event_vols_vol_id_fkey"
          foreign key ("vol_id")
          references "public"."volunteers"
          ("id")
          on update restrict
          on delete cascade;
