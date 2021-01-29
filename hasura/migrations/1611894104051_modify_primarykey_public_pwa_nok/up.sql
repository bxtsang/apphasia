alter table "public"."pwa_nok" drop constraint "pwa_nok_pkey";
alter table "public"."pwa_nok"
    add constraint "pwa_nok_pkey" 
    primary key ( "pwa_id", "email" );
