import sentry_sdk
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.utils import send_email, send_welcome_email


class TimeStamp(models.Model):
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class User(AbstractUser, TimeStamp):
    class SocialProvider(models.TextChoices):
        GOOGLE = "GOOGLE"
        APPLE = "APPLE"

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."  # noqa : E501
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    password = models.CharField(_("password"), max_length=128, null=True)
    social_provider = models.CharField(
        max_length=30,
        choices=SocialProvider.choices,
        default=SocialProvider.GOOGLE,
    )
    is_subscribed = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    @classmethod
    def get_or_create_user(self, email):
        try:
            is_new = False
            user = User.objects.get(username=email)
            if user.deleted_at is not None:
                user.deleted_at = None
                user.save(update_fields=["deleted_at"])
                is_new = True
        except User.DoesNotExist:
            user = User.objects.create(username=email, password="")
            send_welcome_email(
                email,
                user.username,
            )
            is_new = True
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

        return user, is_new

    def delete_user(instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])
        return instance


class Device(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


class PatchNote(models.Model):
    title = models.CharField(max_length=255)
    html_file = models.FileField(upload_to="patch_note/")
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    email_sent = models.BooleanField(default=False)
    email_list = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 모든 사용자에게 이메일 보내기
        if not self.email_sent:  # 이메일이 아직 보내지지 않은 경우
            user_email_list = self.send_email_to_all_users()
            self.email_sent = True  # 이메일을 보냈으므로 True로 변경
            self.email_list = ", ".join(user_email_list)
            self.save(update_fields=["email_sent", "email_list"])

    def send_email_to_all_users(self):
        # 모든 사용자에게 이메일 보내기
        user_email_list = User.objects.filter(
            deleted_at__isnull=True, is_staff=False
        ).values_list("username", flat=True)
        subject = f"OneStep's New Patch Note: {self.title}"
        sentry_sdk.capture_message(
            f"Patch note title : {self.title}, Sending email to users"
        )
        try:
            # HTML 파일 내용 읽기
            with open(self.html_file.path, "r") as f:
                message = f.read()
            send_email(
                to_email_address=list(user_email_list),
                subject=subject,
                message=message,
            )
            return user_email_list
        except Exception as e:
            sentry_sdk.capture_exception(e)
