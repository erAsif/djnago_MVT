from django.contrib.auth.base_user import BaseUserManager
from django.db                  import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin



class CustomUserManager(BaseUserManager):
    """
    CustomUser banane ki factory.
    create_user()      → normal user (hashed password)
    create_superuser() → admin user (is_staff=True, is_superuser=True)
    """

    def create_user(self, email, username, phone,
                       password=None, **extra_fields):
        # Validations
        if not email:
            raise ValueError('Email field is required!')
        if not username:
            raise ValueError('Username is required!')
        if not phone:
            raise ValueError('Phone number is required!')

        # Email normalize  (lowercase + clean domain)
        email = self.normalize_email(email) 

        # create User object 
        user = self.model(
            email    = email,
            username = username,
            phone    = phone,
            **extra_fields
        )
        # Password hash karke set karo (PBKDF2 bcrypt automatically!)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone,password, **extra_fields):

        extra_fields.setdefault('is_staff',     True)  # admin site access
        extra_fields.setdefault('is_superuser', True) # all permissions 
        extra_fields.setdefault('is_active',    True)   # auto-activate superusers

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, phone, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Production-ready Custom User Model.
    ⭐ Login EMAIL se hoga — username se NAHI!
    AbstractBaseUser  → password hashing + auth methods
    PermissionsMixin  → groups, permissions, is_superuser
    """

    # ── Identity Fields ────────────────────────────────────────────
    username = models.CharField(max_length=50, unique=True,error_messages={'unique': "This username is taken."}  )
    email = models.EmailField(unique=True,error_messages={'unique': "This email is already registered."} )
    phone = models.CharField(max_length=15, unique=True, help_text='Format: +91XXXXXXXXXX' )

    # ── Personal Info ──────────────────────────────────────────────
    # first_name = models.CharField(max_length=50, blank=True)
    # last_name  = models.CharField(max_length=50, blank=True)
    dob        = models.DateField(null=True, blank=True, verbose_name="Date of Birth")

    # ── Profile ────────────────────────────────────────────────────
    # profile_img = models.ImageField(
    #     upload_to='profiles/%Y/%m/',  # year/month folders
    #     blank=True, null=True,
    #     default='profiles/default.png'
    # )
    # address = models.TextField(blank=True)
    # bio     = models.TextField(max_length=500, blank=True)

    # ── Status Flags ───────────────────────────────────────────────
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    # ── Timestamps ─────────────────────────────────────────────────
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    # ── Auth Config ────────────────────────────────────────────────
    USERNAME_FIELD  = 'email'         # ⭐ Email se login!
    REQUIRED_FIELDS = ['username', 'phone']  # createsuperuser ke liye

    objects = CustomUserManager()      # hamara custom manager

    class Meta:
        verbose_name        = 'User'
        verbose_name_plural = 'Users'
        ordering            = ['-date_joined']

    def __str__(self):
        return f"{self.username} <{self.email}>"

