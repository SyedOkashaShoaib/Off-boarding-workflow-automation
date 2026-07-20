Select-String `
    -Path app\routes\case_routes.py `
    -Pattern "case_created|case_detail|@case_bp" `
    -Context 2,3