from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator



class CustomUserManager(UserManager):
  use_in_migrations = True
  
  def _create_user(self, username, password, **extra_fields):
    username = self.model.normalize_username(username)
    user = self.model(username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_user(self, username, password=None, **extra_fields):
      extra_fields.setdefault('is_staff', False)
      extra_fields.setdefault('is_superuser', False)
      return self._create_user(username, password, **extra_fields)

  def create_superuser(self, username, password, **extra_fields):
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_superuser', True)
      
      if extra_fields.get("is_staff") is not True:
          raise ValueError('Superuser must have is_staff=True.')
      if extra_fields.get("is_superuser") is not True:
          raise ValueError('Superuser must have is_superuser=True.')
      return self._create_user(username, password, **extra_fields)


class UserDB(AbstractBaseUser, PermissionsMixin):
    """Custom User"""
    class Meta:
        verbose_name = 'UserDB'
        verbose_name_plural = 'UserDB'

    username_validators = UnicodeUsernameValidator()     #不正な文字列が含まれていないかチェック
    username = models.CharField(max_length=15, primary_key=True, unique=True, blank=False, null=False, help_text="学籍番号")
    is_active = models.BooleanField(default=True) # アクティブ権限
    is_staff = models.BooleanField(default=False) # スタッフ権限
    is_superuser = models.BooleanField(default=False) # 管理者権限
    date_joined = models.DateTimeField(default=timezone.now) # アカウント作成日時
    # password_changed = models.BooleanField(default=False, null=True) # パスワードを変更したかどうかのフラグ
    # password_changed_date = models.DateTimeField(null=True) # 最終パスワード変更日時

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['username',]

    def clean(self):
        super().clean()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username


times = (
  (1, '1限目'),
  (2, '2限目'),
  (3, '3限目'),
  (4, '4限目'),
  (5, '5限目'),
  (6, '6限目'),
)
weeks = (
  (1, "月曜日"),
  (2, "火曜日"),
  (3, "水曜日"),
  (4, "木曜日"),
  (5, "金曜日"),
  (6, "土曜日"),
  (7, "日曜日"),
)
sounds = (
    (1, '誰もいなかった'),
    (2, '少しいたが静かだった'),
    (3, '大勢いたが静かだった'),
    (4, '普通'),
    (5, '少しいたがうるさかった'),
    (6, '大勢いてうるさかった'),
)


class RoomDB(models.Model):
    class Meta:
        verbose_name = 'RoomDB'
        verbose_name_plural = 'RoomDB'

    room_number = models.CharField("教室名", max_length=6, primary_key=True, blank=False, null=False, help_text="教室名")
    capacity = models.IntegerField("収容人数", blank=False, null=False, help_text="収容人数")

    # 投稿1つずつの表紙
    def __str__(self):
        return self.room_number


class SolidDB(models.Model):
    class Meta:
        verbose_name = 'SolidDB'
        verbose_name_plural = 'SolidDB'

    day_week = models.IntegerField("曜日", choices=weeks, blank=False, null=False, help_text="曜日")
    room_number = models.CharField("教室名", max_length=6, blank=False, null=False, help_text="教室名")
    time = models.IntegerField("時間割", choices=times, blank=False, null=False, help_text="時間割")
    comment = models.CharField("コメント", max_length=255, blank=True, null=True, help_text="コメント")

    # 投稿1つずつの表紙
    def __str__(self):
        return self.room_number


class TemporaryDB(models.Model):
    class Meta:
        verbose_name = 'TemporaryDB'
        verbose_name_plural = 'TemporaryDB'

    room_number = models.CharField("教室名", max_length=6, blank=False, null=False, help_text="教室名")
    time = models.IntegerField("時間割", choices=times, blank=False, null=False, help_text="時間割")
    student_reserved = models.IntegerField("学生予約", blank=False, null=False, default=0, help_text="学生予約(学生予約でないなら0学生予約なら人数)")
    date = models.DateField("日付", blank=False, null=False, help_text="日付")
    
    # 投稿1つずつの表紙
    def __str__(self):
        return self.room_number


class AssetDB(models.Model):
    class Meta:
        verbose_name = 'AssetDB'
        verbose_name_plural = 'AssetDB'

    student_number = models.CharField("学籍番号", max_length=11, blank=False, null=False, help_text="学籍番号")
    room_number = models.CharField("教室名", max_length=6, blank=False, null=False, help_text="教室名")
    time = models.IntegerField("時間割", choices=times, blank=False, null=False, help_text="時間割")
    date = models.DateField("日付", blank=False, null=False, auto_now=True, help_text="日付")
    use_num = models.IntegerField("利用人数", blank=False, null=False, help_text="利用人数")
    sound = models.IntegerField("騒音度", choices=sounds, blank=False, null=False, help_text="騒音度")
    
    # 投稿1つずつの表紙
    def __str__(self):
        return self.student_number