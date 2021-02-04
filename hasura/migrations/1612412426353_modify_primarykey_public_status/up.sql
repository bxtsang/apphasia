alter table "public"."status" drop constraint "vol_status_pkey";
alter table "public"."status"
    add constraint "status_pkey" 
    primary key ( "description" );
