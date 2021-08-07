from django.contrib.admin.sites import site
import os


admin_site = site
admin_site.login_template = os.path.join('app', 'common', 'login.html')
admin_site.site_title = "Aone Site Admin"
admin_site.site_header = "Aone clients website adminstration"
admin_site.index_title = "Website content site adminstration"
