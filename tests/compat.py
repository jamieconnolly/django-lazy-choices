import django


def run_model_admin_check(model_admin, model):
    if django.VERSION >= (1, 9):
        from django.contrib.admin.sites import site
        return model_admin(model, site).check()
    else:
        return model_admin.check(model=model)
