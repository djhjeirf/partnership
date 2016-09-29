from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                    (r'^$', 'chairman.views.login'),
                       (r'^login', 'chairman.views.login'),
                       (r'^logout', 'chairman.views.logout'),
                       (r'^db_tables_list', 'chairman.views.db_page'),

                       (r'^land_category/(?P<id>.+)', 'chairman.views.change_land_category'),
                       (r'^plot/(?P<id>.+)', 'chairman.views.change_plot'),
                       (r'^use_case/(?P<id>.+)', 'chairman.views.change_use_case'),
                       (r'^owner/(?P<id>.+)', 'chairman.views.change_owner'),

                       (r'^add_plot', 'chairman.views.add_plot'),
                       (r'^add_land_category', 'chairman.views.add_land_category'),
                       (r'^add_use_case', 'chairman.views.add_use_case'),
                       (r'^add_owner', 'chairman.views.add_owner'),

                       (r'^delete_land_category/(?P<id>.+)', 'chairman.views.delete_land_category'),
                       (r'^delete_use_case/(?P<id>.+)', 'chairman.views.delete_use_case'),
                       (r'^delete_plot/(?P<id>.+)', 'chairman.views.delete_plot'),
                       (r'^delete_owner/(?P<id>.+)', 'chairman.views.delete_owner'),


                       (r'^save_land_category', 'chairman.views.save_land_category'),
                       (r'^save_use_case', 'chairman.views.save_use_case'),
                       (r'^save_plot', 'chairman.views.save_plot'),
                       (r'^save_owner', 'chairman.views.save_owner'),

                       (r'^land_categories_list', 'chairman.views.list_land_categories'),
                       (r'^use_cases_list', 'chairman.views.list_use_cases'),
                       (r'^plots_list', 'chairman.views.list_plots'),
                       (r'^owners_list', 'chairman.views.list_owners'),
)
