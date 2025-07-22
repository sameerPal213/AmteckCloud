# trello/models.py

from django.db import models
import random
import string


class Enterprise(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=False, 
                        null=False, 
                        unique=True)
    name        = models.CharField(max_length=50,
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=False,
                        default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed     = True
        db_table    = "Bronze].[trello_enterprise"
        ordering    = ["name"]

    def __str__(self):
        return self.name


class Workspace(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=False, 
                    null=False, 
                    unique=True)
    enterprise  = models.ForeignKey(
                    Enterprise, 
                    on_delete=models.CASCADE,
                    null=True)
    name        = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=False,
                    default='')
    display_name = models.CharField(
                    max_length=200,
                    blank=True,
                    null=False,
                    default='')
    description = models.CharField(max_length=500, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=False,
                    default='')
    url         = models.URLField( 
                    blank=True, 
                    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "Bronze].[trello_workspace"
        ordering    = ["display_name"]

    def __str__(self):
        return self.display_name


class Member(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(max_length=50, blank=False, null=False, 
                    unique=True)
    enterprise  = models.ForeignKey(
                    Enterprise, 
                    on_delete=models.CASCADE,
                    null=True,
                    blank=True)
    workspaces  = models.ManyToManyField(Workspace, blank=True)
    username    = models.CharField(
                    max_length=50, 
                    blank=True, 
                    null=False,
                    default='')
    email       = models.CharField(
                    max_length=500,
                    blank=True, 
                    null=False, 
                    default='')
    full_name   = models.CharField(
                    max_length=50, 
                    blank=True, 
                    null=False,
                    default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "Bronze].[trello_member"
        ordering    = ["full_name"]

    def __str__(self):
        return "{} ({})".format(self.full_name, self.trello_id)


class Board(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=False, 
                    null=False, 
                    unique=True)
    workspace   = models.ForeignKey(
                    Workspace,
                    on_delete=models.CASCADE,
                    null=True)
    members     = models.ManyToManyField(Member)
    name        = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=False,
                    default='')
    description = models.TextField(
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    desc_data   = models.TextField(
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    closed      = models.IntegerField(blank=True, null=True)
    pinned      = models.IntegerField(blank=True, null=True)
    url         = models.URLField( 
                    blank=True, 
                    null=True)
    short_url   = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=False,
                    default='')
    prefs       = models.TextField(
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'Bronze].[trello_board'
        ordering    = ["name"]

    def __str__(self):
        return '{} ({})'.format(self.name, self.trello_id)


class Label(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=False, 
                    null=False)
    board       = models.ForeignKey(
                    Board,
                    on_delete=models.CASCADE,
                    null=True)
    name        = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=False,
                    default='')
    color       = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "Bronze].[trello_label"
        ordering    = ["name"]

    def __str__(self):
        return "{} ({})".format(self.name, self.trello_id)


class List(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=False, 
                    null=False)
    board       = models.ForeignKey(
                    Board,
                    on_delete=models.CASCADE,
                    null=True)
    name        = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=False,
                    default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'Bronze].[trello_list'
        ordering    = ["name"]

    def __str__(self):
        return "{} ({})".format(self.name, self.trello_id)


class Card(models.Model):
    id              = models.AutoField(primary_key=True)
    trello_id       = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=False, 
                        null=False, 
                        unique=True)
    board           = models.ForeignKey(
                        Board, 
                        on_delete=models.CASCADE, 
                        null=True)
    list            = models.ForeignKey(
                        List, 
                        on_delete=models.CASCADE, 
                        null=True)
    labels          = models.ManyToManyField(Label)
    members         = models.ManyToManyField(Member)
    address         = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    location        = models.CharField(max_length=10, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    badges_location = models.IntegerField(blank=True, null=True)
    badges_votes    = models.IntegerField(blank=True, null=True)
    badges_viewing_member_voted = models.IntegerField(blank=True, null=True)
    badges_subscribed = models.IntegerField(blank=True, null=True)
    badges_fogbugz  = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    badges_check_items = models.IntegerField(blank=True, null=True)
    badges_check_items_checked = models.IntegerField(blank=True, null=True)
    badges_comments = models.IntegerField(blank=True, null=True)
    badges_attachments = models.IntegerField(blank=True, null=True)
    badges_description = models.IntegerField(blank=True, null=True)
    badges_due      = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    badges_start    = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    badges_due_complete = models.IntegerField(blank=True, null=True)
    check_item_states = models.TextField(
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    closed          = models.IntegerField(blank=True, null=True)
    coordinates     = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    creation_method = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    date_last_activity = models.DateField(blank=True, null=True)
    description     = models.CharField(
                        max_length=2000,
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    description_data = models.TextField(
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    due             = models.DateTimeField(blank=True, null=True)
    due_reminder    = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    email           = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    id_short        = models.IntegerField(blank=True, null=True)
    id_attachment_cover = models.CharField(max_length=36, 
                        blank=True, 
                        null=True)
    location_name   = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    manual_cover_attachment = models.IntegerField(blank=True, null=True)
    name            = models.TextField(
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    pos             = models.IntegerField(blank=True, null=True)
    short_link      = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    short_url       = models.CharField(max_length=50, 
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    url             = models.URLField( 
                        blank=True, 
                        null=True)
    cover           = models.TextField(
                        db_collation='SQL_Latin1_General_CP1_CI_AS', 
                        blank=True, 
                        null=True)
    start           = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "Bronze].[trello_card"
        ordering    = ["name"]

    def __str__(self):
        return "{} ()".format(self.name)


class Checklist(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=False, 
                    null=False)
    card        = models.ForeignKey(
                    Card, 
                    on_delete=models.CASCADE, 
                    null=True)
    name        = models.CharField(
                    max_length=200,
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'Bronze].[trello_checklist'

    def __str__(self):
        return self.name


class CustomField(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(
                    max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=False, 
                    null=False)
    board       = models.ForeignKey(
                    Board, 
                    on_delete=models.CASCADE, 
                    null=True)
    name        = models.CharField(
                    max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    type        = models.CharField(
                    max_length=50,
                    blank=True,
                    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "Bronze].[trello_customfield"

    def __str__(self):
        return self.name


class CheckItem(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(
                    max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=False, 
                    null=False)
    checklist   = models.ForeignKey(
                    Checklist, 
                    on_delete=models.CASCADE,
                    null=True)
    name        = models.TextField(
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    state       = models.CharField(
                    max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    due         = models.DateField(auto_now=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "Bronze].[trello_checkitem"

    def __str__(self):
        return self.name


# These are the possible values for a dropdown custom field
class CustomFieldOption(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(
                    max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=False, 
                    null=False)
    CustomField = models.ForeignKey(
                    CustomField, 
                    on_delete=models.CASCADE,
                    null=True)
    value       = models.CharField(
                    max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "Bronze].[trello_customfieldoption"

    def __str__(self):
        return self.trello_id


class CustomFieldItem(models.Model):
    id                  = models.AutoField(primary_key=True)   
    trello_id           = models.CharField(
                            max_length=50, 
                            db_collation='SQL_Latin1_General_CP1_CI_AS', 
                            blank=False, 
                            null=False)
    card                = models.ForeignKey(
                            Card, 
                            on_delete=models.CASCADE,
                            null=True)
    customField         = models.ForeignKey(
                            CustomField, 
                            on_delete=models.CASCADE,
                            null=True)
    customFieldOption   = models.ForeignKey(
                            CustomFieldOption, 
                            on_delete=models.CASCADE,
                            null=True)
    value               = models.TextField(
                            db_collation='SQL_Latin1_General_CP1_CI_AS', 
                            blank=True, 
                            null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "Bronze].[trello_customfielditem"

    def __str__(self):
        return self.trello_id


class Webhook(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(
                    max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=False, 
                    null=False)
    description = models.TextField(
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    model_id    = models.CharField(
                    max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    model_type  = models.CharField(
                    max_length=50, 
                    db_collation='SQL_Latin1_General_CP1_CI_AS', 
                    blank=True, 
                    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "Bronze].[trello_webhook"

    def __str__(self):
        return self.description


class Action(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(max_length=50, blank=False, null=False)
    webhook     = models.ForeignKey(
                    Webhook, 
                    on_delete=models.CASCADE,
                    null=True)
    member      = models.ForeignKey(
                    Member, 
                    on_delete=models.CASCADE,
                    null=True)
    data        = models.TextField(blank=True, null=True)
    creator     = models.CharField(max_length=50, blank=True, null=True)
    type        = models.CharField(max_length=50, blank=True, null=True)
    date        = models.DateField(auto_now=False, blank=True, null=True)
    limits      = models.TextField(blank=True, null=True)
    display     = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = "Bronze].[trello_action"

    def __str__(self):
        return self.trello_id
    
    
class MissingAction(models.Model):
    id      = models.AutoField(primary_key=True)
    type    = models.CharField(
            max_length=50, 
            db_collation='SQL_Latin1_General_CP1_CI_AS', 
            blank=True, 
            null=True)
    data    = models.TextField(
            db_collation='SQL_Latin1_General_CP1_CI_AS', 
            blank=True, 
            null=True)
    display = models.TextField(
            db_collation='SQL_Latin1_General_CP1_CI_AS', 
            blank=True, 
            null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        managed = True
        db_table = 'Bronze].[trello_missingaction'

    def __str__(self):
        return self.id


class Comment(models.Model):
    id          = models.AutoField(primary_key=True)
    trello_id   = models.CharField(max_length=50, blank=False, null=False)
    text        = models.TextField(blank=True, null=True)
    card        = models.ForeignKey(Card, on_delete=models.CASCADE, null=True)
    date        = models.DateTimeField(default="1999-12-30 12:00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "Bronze].[trello_comment"

    def __str__(self):
        self.trello_id
