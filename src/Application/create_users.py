from django.contrib.auth import get_user_model
UserModel = get_user_model()
if not UserModel.objects.filter(username='admin_retail').exists():
    user = UserModel.objects.create_user(
        'admin_retail', password='examExam%99')
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.save()
if not UserModel.objects.filter(username='user_1').exists():
    user = UserModel.objects.create_user('user_1', password='examExam_1')
    user.is_superuser = False
    user.is_staff = False
    user.is_active = True
    user.save()
if not UserModel.objects.filter(username='user_2').exists():
    user = UserModel.objects.create_user('user_2', password='examExam_2')
    user.is_superuser = False
    user.is_staff = False
    user.is_active = True
    user.save()
