# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.




class Group(models.Model):
    label = models.CharField(max_length=50)
    max = models.IntegerField(null=True)

    def __unicode__(self):
        return self.label


class Card(models.Model):
    label = models.CharField(max_length=20)
    group = models.ForeignKey(Group, null=True)

    def __unicode__(self):
        return "{} ({})".format(self.label, self.group)


class Device(models.Model):
    code = models.CharField(max_length=2, null=True)
    label = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return "{} ({})".format(self.label, self.code)


class RegistrationManager(models.Manager):

    def register(self, s_datetime, s_dev, s_card, filename):
        mkph = False
        o_card, created = Card.objects.get_or_create(label=s_card)
        qi = Duration.objects.filter(card=o_card, registration_out__isnull=True)

        if o_card.group:
            max_cnt = o_card.group.max
            cur_cnt = Duration.objects.filter(card__group=o_card.group, registration_out__isnull=True).count()
        else:
            max_cnt = 0
            cur_cnt = 0

        avaible = max_cnt - cur_cnt

        q = self.filter(datetime=s_datetime)
        if not q:
            mkph = True
            o_dev, created = Device.objects.get_or_create(code=s_dev)
            o_reg = self.create(datetime=s_datetime, card=o_card, device=o_dev, group=o_card.group, img="photoes/"+filename)

            if qi:
                for x in qi:
                    x.registration_out = o_reg
                    x.save()

                direction = "Out"
                action = "Ok"

            else:
                direction = "In"
                if cur_cnt < max_cnt:
                    action = "Accept"
                    Duration.objects.create(card=o_card, registration_in=o_reg)
                else:
                    action = "Decline"

            o_reg.action = action
            o_reg.direction = direction
            o_reg.save()

        else:
            #for last state
            o_reg = q.first()
            if qi:
                direction = "In"
                if cur_cnt > max_cnt:
                    action = "Decline"
                else:
                    action = "Accept"
            else:
                action = o_reg.action
                direction = o_reg.direction

        return o_card, direction, max_cnt, action, avaible, mkph


class Registration(models.Model):
    objects = RegistrationManager()

    datetime = models.DateTimeField(null=True)
    registration_datetime = models.DateTimeField(auto_now=True)
    card = models.ForeignKey(Card, null=True)
    device = models.ForeignKey(Device, null=True)
    action = models.CharField(max_length=10, null=True)
    direction = models.CharField(max_length=10, null=True)
    img = models.ImageField(upload_to = 'photoes', null=True)
    group = models.ForeignKey(Group, null=True)

    def __unicode__(self):
        return "{}, {}, {}".format(self.datetime, self.card, self.device)

    def image_tag(self):
        return u'<img src="/media/%s" />' % self.img

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class Duration(models.Model):
    card = models.ForeignKey(Card, null=True)
    registration_in = models.ForeignKey(Registration, null=True)
    registration_out = models.ForeignKey(Registration, null=True, related_name='registration2registration_out')
    duration = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if self.registration_out:
            timedelta = self.registration_out.datetime - self.registration_in.datetime.replace(tzinfo=None)
            self.duration = timedelta.days*86400 + timedelta.seconds
        return super(Duration, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{}, {}: {}s".format(self.registration_in.datetime, self.card, self.duration)
