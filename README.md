####################################################giving assess to staff or superuser

from django.contrib.auth import get_user_model

# Retrieve the user model
User = get_user_model()

# Retrieve and update the user
try:
    user = User.objects.get(username='FINANCE')
    user.is_staff = True        # Allow access to the admin site
    user.is_superuser = False   # Grant superuser privileges
    user.save()
    print("User permissions updated successfully!")
except User.DoesNotExist:
    print("User not found.")


###################################################### Delete All Departments

from app.models import Department

# Delete all departments
Department.objects.all().delete()
print("All departments deleted.")


###################################################### Delete All Department Heads

from app.models import DepartmentHead

# Delete all department heads
DepartmentHead.objects.all().delete()
print("All department heads deleted.")


####################################################### Assign heads to departments

from django.contrib.auth import get_user_model
from app.models import Department, DepartmentHead

User = get_user_model()

# Ensure Departments Exist
hr, created = Department.objects.get_or_create(name="HR")
tr, created = Department.objects.get_or_create(name="TR")
finance, created = Department.objects.get_or_create(name="FINANCE")

# Ensure Users Exist
user1, created = User.objects.get_or_create(username="HR", defaults={"password": "pass@321"})
user2, created = User.objects.get_or_create(username="TR", defaults={"password": "pass@321"})
user2, created = User.objects.get_or_create(username="FINANCE", defaults={"password": "pass@321"})


# Assign Department Heads
DepartmentHead.objects.create(user=user1, department=hr)
DepartmentHead.objects.create(user=user2, department=tr)
DepartmentHead.objects.create(user=user2, department=finance)
