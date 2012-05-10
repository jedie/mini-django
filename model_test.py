#!/usr/bin/env python
# coding: utf-8

"""
Self contained django app to play with models.
    
Output from this current example code:


___________________________________________________________________
 *** call 'syncdb':
Creating tables ...
Creating table auth_permission
Creating table auth_group_permissions
Creating table auth_group
Creating table auth_user_user_permissions
Creating table auth_user_groups
Creating table auth_user
Creating table auth_testmodel
Creating table django_content_type
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)
___________________________________________________________________
 *** play with the models:
new instance: TestModel entry: 'test'

print instance data:

           id: None
 date_created: None
  last_update: None
         user: <User: test>
      content: 'test'

some instance data after save:

pk: 1
create date: 2012-05-10T08:10:08.748351
last update: 2012-05-10T08:10:08.748378
-------------------------------------------------------------------------------
- END -   
"""

import os

APP_LABEL = os.path.splitext(os.path.basename(__file__))[0]

os.environ["DJANGO_SETTINGS_MODULE"] = APP_LABEL

# SETTINGS:
DEBUG = TEMPLATE_DEBUG = True

# insert other apps if needed:
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    APP_LABEL,
)

# use memory SQLite database:
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

if __name__ == "__main__":
    #______________________________________________________________________________
    # example TestModel model classes:

    from django.db import models
    from django.contrib.auth.models import User

    class TestModel(models.Model):
        date_created = models.DateTimeField(auto_now_add=True)
        last_update = models.DateTimeField(auto_now=True)
        user = models.ForeignKey(User, blank=True, null=True)
        content = models.TextField()

        def __unicode__(self):
            return u"TestModel entry: '%s'" % self.content

        class Meta:
            app_label = "auth"  # Hack: Cannot use an app_label that is under South control, due to http://south.aeracode.org/ticket/520

    print "___________________________________________________________________"
    print " *** call 'syncdb':"

    from django.core import management
    management.call_command('syncdb', verbosity=1, interactive=False)

    print "___________________________________________________________________"
    print " *** play with the models:"

    # create a test user:
    user = User(username="test")
    user.save()

    # create new instance:
    instance = TestModel(content="test", user=user)
    print "new instance:", instance

    print "\nprint instance data:\n"
    for field in instance._meta.fields:
        print "%13s: %s" % (field.name, repr(getattr(instance, field.name)))

    instance.save()
    print "\nsome instance data after save:\n"
    print "pk:", instance.pk
    print "create date:", instance.date_created.isoformat()
    print "last update:", instance.last_update.isoformat()

    print "-"*79
    print "- END -"
