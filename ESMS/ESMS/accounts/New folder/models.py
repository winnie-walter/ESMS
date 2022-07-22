from django.db import models

# Create your models here.


from django.contrib.auth.models import User


class Users():
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def add_user(self):
        return self.username

    def edit_user(self):
        pass

    def delete_user(self):
        pass

    def deactivate_user(self):
        pass

    def search_user(self):
        pass

    def assign_role(self):
        pass


class Admins():
    GENDER = (('Male', 'MALE'),
              ('Female', 'FEMALE'), ('Others', 'Others')
              )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile = models.ImageField(upload_to='profile_pic', default='default.jpg', null=True, blank=True)


class EventType():
    name = models.CharField(max_length=100)

    def add_eventtype(self):
        return self.username

    def edit_eventtype(self):
        pass

    def delete_eventtype(self):
        pass


    def search_eventtype(self):
        pass


class Event():
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    time = models.TimeField()
    card = models.ImageField(upload_to='cards', null=True, blank=True)
    qrcode = models.ImageField(upload_to='eventqrcode', null=True, blank=True)
    eventtype = models.ForeignKey(EventType, on_delete=models.CASCADE)
    user = models.ForeignKey(Admins, on_delete=models.CASCADE)

    def add_event(self):
        return self.username

    def edit_event(self):
        pass

    def delete_event(self):
        pass

    def search_event(self):
        pass


class Guest():
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def add_guest(self):
        return self.username

    def edit_guest(self):
        pass

    def delete_guest(self):
        pass

    def search_guest(self):
        pass
