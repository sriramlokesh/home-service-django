from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from HomeServices_app import views
from HomeServices_project import settings
from django.contrib.auth.views import (
    # LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from . import views
from .forms import stateform
from .views import *

urlpatterns = [
    path('', views.home.as_view(), name='index'),
    path('index/', views.home.as_view(), name='index_page'),
    path('choose-login/', views.ChooseLogin.as_view(), name='choose_login'),
    path('login/', views.Login.as_view(), name='login_page'),
    path('logout', views.logout_view, name='logout'),
    path('user_registration/', views.User_Register.as_view(), name='user_registration'),
    path('Worker_Register/', views.Worker_Register.as_view(), name='Worker_Register'),
    path('admin_registration/', views.AdminRegistration.as_view(), name='admin_registration'),
    path('about/',views.about.as_view(),name='about'),
    path('services/',views.services.as_view(),name='services'),
    path('contact/',views.contact.as_view(),name='contact'),
    path('bookservice/<int:id>',views.bookservice.as_view(),name='bookservice'),

    # Super Admin URLs
    path('super-admin-login/', views.SuperAdminLogin.as_view(), name='super_admin_login'),
    path('super_admin_dashboard/', views.SuperAdminDashboard.as_view(), name='super_admin_dashboard'),
    path('admin-request-action/<int:request_id>/<str:action>/', views.AdminRequestAction.as_view(), name='admin_request_action'),
    path('admin-edit/<int:request_id>/', views.AdminEditView.as_view(), name='admin_edit'),

    # Regular Admin Login
    path('admin-login/', views.AdminLogin.as_view(), name='admin_login'),

    path('admmin_home/', views.admmin_home.as_view(), name='admmin_home'),
    path('workers_home/', views.workers_home.as_view(), name='workers_home'),



    path('manageworker/', views.manageworker.as_view(), name='manageworker'),
    path('manageusers/', views.manageusers.as_view(), name='manageusers'),
    path('verify_worker/<str:action>/<int:id>',views.verify_worker.as_view(),name='verify_worker'),
    path('delete_worker/<int:id>',views.DeleteWorker.as_view(),name='delete_worker'),

    path('AddCountry/', views.AddCountry.as_view(), name='AddCountry'),
    path('ManageCountry/', views.ManageCountry.as_view(), name='ManageCountry'),
    path('DeleteCountry/<int:id>',views.DeleteCountry.as_view(),name='DeleteCountry'),

    path('AddCity/', views.AddCity.as_view(), name='AddCity'),
    path('managecity/', views.managecity.as_view(), name='managecity'),
    path('DeleteCity/<int:id>',views.DeleteCity.as_view(),name='DeleteCity'),

    path('AddState/', views.AddState.as_view(), name='AddState'),
    path('ManageState/', views.ManageState.as_view(), name='ManageState'),
    path('DeleteState/<int:id>',views.DeleteState.as_view(),name='DeleteState'),


    path('AddServices/', views.AddServices.as_view(), name='AddServices'),
    path('ManageServices/', views.ManageServices.as_view(), name='ManageServices'),
    path('DeleteServices/<int:id>',views.DeleteServices.as_view(),name='DeleteServices'),
    path('EditServices/<int:id>',views.EditServices.as_view(),name='EditServices'),

    path('AssignWorker/<int:id>',views.AssignWorker.as_view(),name='AssignWorker'),
   

    path('feedback_form/', views.feedback_form.as_view(), name='feedback_form'),
    path('viewfeedbacks/', views.viewfeedbacks.as_view(), name='viewfeedbacks'),
    path('ViewRequests/', views.ViewRequests.as_view(), name='ViewRequests'),
    path('viewresponse/',views.viewresponse.as_view(),name='viewresponse'),

    
    path('Viewappointment_history/',views.Viewappointment_history.as_view(),name='Viewappointment_history'),
    path('CancelRequest/<int:id>',views.CancelRequest.as_view(),name='CancelRequest'),
    path('userprofile/',views.userprofile.as_view(),name='userprofile'),
    path('workerprofile/',views.workerprofile.as_view(),name='workerprofile'),
    path('edit_worker_profile/', views.EditWorkerProfile.as_view(), name='edit_worker_profile'),
   



    path('ViewColleagues/', views.ViewColleagues.as_view(), name='ViewColleagues'),
    path('WorkerViewRequests/', views.WorkerViewRequests.as_view(), name='WorkerViewRequests'),
    path('viewworkerfeedbacks/', views.viewworkerfeedbacks.as_view(), name='viewworkerfeedbacks'),
    path('WorkerpendingTask/',views.workerviewresponse.as_view(),name='WorkerpendingTask'),

    path('acceptrequest/<str:action>/<int:id>',views.acceptrequest.as_view(),name='acceptrequest'),
    path('markcompleted/<str:action>/<int:id>',views.markcompleted.as_view(),name='markcompleted'),
    path('reject/<str:action>/<int:id>',views.reject.as_view(),name='reject'),
    

    # path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'),name='password-reset'),
    path('password-reset/',PasswordResetView.as_view(template_name='password_reset.html',html_email_template_name='password_reset_email.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

    path('sales/add/<str:category>/', views.AddProductView.as_view(), name='add_product'),
    path('sales/products/', views.ProductListView.as_view(), name='product_list'),
    path('sales/products/<str:category>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('sales/products/edit/<int:pk>/', views.ProductEditView.as_view(), name='edit_product'),
    path('sales/products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),

    path('sales/grocery/add/', views.AddProductView.as_view(), {'category': 'grocery'}, name='add_grocery_product'),
    path('sales/grocery/manage/', views.ProductListView.as_view(), {'category': 'grocery'}, name='manage_grocery_products'),
    path('sales/electricals/add/', views.AddProductView.as_view(), {'category': 'electricals'}, name='add_electricals_product'),
    path('sales/electricals/manage/', views.ProductListView.as_view(), {'category': 'electricals'}, name='manage_electricals_products'),
    path('sales/plumbing/add/', views.AddProductView.as_view(), {'category': 'plumbing'}, name='add_plumbing_product'),
    path('sales/plumbing/manage/', views.ProductListView.as_view(), {'category': 'plumbing'}, name='manage_plumbing_products'),

    path('sales/<str:category>/', views.SalesCategoryView.as_view(), name='sales_category'),

    path('shop/', views.ShopView.as_view(), name='shop'),
    path('shop/<int:shop_id>/products/', views.ShopProductsView.as_view(), name='shop_products'),
    path('sales/<str:category>/add_shop/', views.AddShopView.as_view(), name='add_shop'),
    path('shop/<int:shop_id>/add_product/', views.AddProductToShopView.as_view(), name='add_product_to_shop'),
    path('shop/<int:shop_id>/edit/', views.EditShopView.as_view(), name='edit_shop'),
    path('sales/<str:category>/manage_shops/', views.ManageShopsView.as_view(), name='manage_shops'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)