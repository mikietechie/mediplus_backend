from django.contrib.admin.sites import site
import os


admin_site = site
#admin_site.login_template = os.path.join('app', 'login.html')
admin_site.site_title = "Mediplus Admin"
admin_site.site_header = "Mediplus Content Admin"
admin_site.index_title = "Mediplus Admin | Home"
