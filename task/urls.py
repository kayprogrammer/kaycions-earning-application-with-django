from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
#----------------------------------------------------------------------------------------------------------
#----------------------GENERAL HOME FAQS REGISTER LOGIN PASSWORD RESET ---------------------------------------------
#----------------------------------------------------------------------------------------------------------

    path('', views.home, name="home"),
    path('faqs/', views.faqs, name="faqs"),
    path('terms/', views.terms, name="terms"),

    path('register/', views.registerPage, name="register"),
    path('<str:ref_code>/register/', views.registerPage2, name="register-ref"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('edit_profile/', views.profile_edit, name="edit_profile"),
    path('my_profile/', views.profile, name="profile"),
    path('help_centre/', views.helpcentre, name="help_centre"),    
    path('withdrawal/', views.withdrawal, name="withdrawal"),
    path('validate-fullname', csrf_exempt(views.FullnameValidatorView.as_view()), name='validate-fullname'),
    path('validate-email', csrf_exempt(views.EmailValidatorView.as_view()), name='validate-email'),
    path('validate-password', csrf_exempt(views.PasswordValidatorView.as_view()), name='validate-password'),
    path('validate-refcode', csrf_exempt(views.ReferralcodeValidatorView.as_view()), name='validate-refcode'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name="activate"),
    
    # PASSWORD RESET
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="task/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="task/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="task/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="task/password_reset_done.html"), name="password_reset_complete"),

#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
#----------------------ALL ADMIN STUFFS-------------------------------------------------------------------
    #TASKS AND WORKERS LISTS AND DETAILS
    path('dashboard/', views.dashboard, name="dashboard"),
    path('worker/<str:pk_test>/', views.worker, name="worker"),
    path('workers/', views.workers, name="workers"),
    path('tasks/', views.tasks, name="tasks"),
    path('pending_tasks/', views.pending_tasks, name="pending_tasks"),
    path('verified_tasks/', views.verified_tasks, name="verified_tasks"),
    path('disapproved_tasks/', views.disapproved_tasks, name="disapproved_tasks"),
    #-----------------------------
    
    #TASK CRUD
    path('create_task/', views.createTask, name="create_task"),
    path('update_task/<str:pk>/', views.updateTask, name="update_task"),
    path('delete_task/<str:pk>/', views.deleteTask, name="delete_task"),
    #----------------------------

    #TASK STATUS UPDATE
    path('verify_task/<int:task_pk>/', views.verify_task, name="verify_task"),
    path('disapprove_task/<int:task_pk>/', views.disapprove_task, name="disapprove_task"),
    path('withdrawal_requests/', views.withdrawalrequests, name="withdrawalrequests"),
    #----------------------

    #PAYMENT STUFFS
    path('verify_payment/<int:withdrawal_pk>/', views.approvewithdrawalrequests, name="verify_payment"),
    path('pending_withdrawalrequests/', views.pending_withdrawalrequests, name="pending_withdrawalrequests"),
    path('verified_withdrawalrequests/', views.verified_withdrawalrequests, name="verified_withdrawalrequests"),
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
#--------------ALL WORKERS STUFF----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
    path('my_dashboard/', views.userPage, name="user-page"),
    path('deletetask/<str:pk>/', views.deleteYourTask, name="delete_your_task"),
    path('attempt_task/<str:pk>/', views.attemptTask, name="attempttask"),
    path('my_pending_tasks/', views.worker_pending_tasks, name="worker_pending_tasks"),
    path('my_verified_tasks/', views.worker_verified_tasks, name="worker_verified_tasks"),
    path('my_disapproved_tasks/', views.worker_disapproved_tasks, name="worker_disapproved_tasks"),
    path('unattempted_tasks/', views.unattemptedtask, name="unattempted_tasks"),
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
#--------------------------ALL NOTIFICATIONS URLS-----------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
    path('notification/<int:notification_pk>/terms/', views.WelcomeNotification.as_view(), name="welcome-notification"),
    path('notification/<int:notification_pk>/earnings/', views.ReferralNotification.as_view(), name="referral-notification"),
    path('notification/<int:notification_pk>/tasks/', views.NewWorkerNotification.as_view(), name="new-worker-notification"),
    path('notification/<int:notification_pk>/unattempted_tasks/', views.TaskNotification.as_view(), name="new-task-notification"),
    path('notification/<int:notification_pk>/pending_tasks/', views.TaskUpdateNotification.as_view(), name="update-task-notification"),
    path('notification/<int:notification_pk>/pending/', views.TaskAttemptNotification.as_view(), name="attempt-task-notification"),
    path('notification/<int:notification_pk>/verified_tasks/', views.TaskVerifiedNotification.as_view(), name="verify-task-notification"),
    path('notification/<int:notification_pk>/disapproved_tasks/', views.TaskDisapproveNotification.as_view(), name="disapprove-task-notification"),
    path('notification/<int:notification_pk>/withdrawal_request/', views.WithdrawalRequestNotification.as_view(), name="withdrawal-request-notification"),
    path('notification/<int:notification_pk>/withdrawal_paid/', views.WithdrawalEarningsPaidNotification.as_view(), name="withdrawal-earnings-paid-notification"),
    path('notification/<int:notification_pk>/admin_pending_tasks/', views.PendingTaskAdminNotification.as_view(), name="pending-task-admin-notification"),
    path('notification/<int:notification_pk>/admin_withdrawal_requests/', views.WithdrawalRequestAdminNotification.as_view(), name="withdrawal-request-admin-notification"),

    path('notification/mark_all_as_read/', views.MarkReadView.as_view(), name="mark_read"),
    path('notification/delete/<int:notification_pk>', views.RemoveNotification.as_view(), name='notification-delete'),
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

]
