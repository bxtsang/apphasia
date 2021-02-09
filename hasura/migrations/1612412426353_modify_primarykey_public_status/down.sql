alter table "public"."status" drop constraint "status_pkey";
alter table "public"."status"
    add constraint "vol_status_pkey" 
    primary key ( "status" );
