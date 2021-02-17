alter table "public"."event_vols" drop constraint "event_vols_pkey";
alter table "public"."event_vols"
    add constraint "event_vols_pkey" 
    primary key ( "vol_id", "event_id" );
