domain = "apphasia.cf"
region = "ap-southeast-1"
hasura_admin_secret = "pwayismyhome12061997"
hasura_jwt_secret_algo = "RS256"
hasura_jwt_secret_key = <<EOT
    {
        "type":"RS256",
        "jwk_url": "https://cognito-idp.ap-southeast-1.amazonaws.com/ap-southeast-1_0wc22ewSD/.well-known/jwks.json",
        "claims_format": "stringified_json"
    }
    EOT
rds_username = "aphasiaSGuser"
rds_password = "aphasiaSGpassword"
ecs_cluster_name = "hasura-prod-cluster"