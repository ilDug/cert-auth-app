cors_mw_config = {
    "allow_credentials": True,
    "allow_origins": [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    "allow_methods": ["OPTIONS", "POST", "PUT", "GET", "DELETE"],
    "expose_headers": [
        "Origin",
        "Content-Type",
        "Set-Cookie",
        "X-Error",
        "X-Auth-Token",
        "Authorization",
        "X-Dag-Head"
        # "Access-Control-Expose-Headers"
    ],
    "allow_headers": [
        "Origin",
        "Content-Type",
        "Set-Cookie",
        "X-Error",
        "Accept",
        "Authorization",
        # "Access-Control-Expose-Headers"
    ],
}
