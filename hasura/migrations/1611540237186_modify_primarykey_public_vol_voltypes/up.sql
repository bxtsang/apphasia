alter table "public"."vol_voltypes" drop constraint "vol_voltypes_pkey";
alter table "public"."vol_voltypes"
    add constraint "vol_voltypes_pkey" 
    primary key ( "vol_id", "voltype" );
