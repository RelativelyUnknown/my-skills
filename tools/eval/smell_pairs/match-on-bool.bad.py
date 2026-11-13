def label(is_admin):
    match is_admin:
        case True:
            return "admin"
        case False:
            return "user"
