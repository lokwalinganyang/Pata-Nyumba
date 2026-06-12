from django.db import models
from django.contrib.auth.models import User

class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    alt_phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Location(models.Model):
    LOCATION_TYPES = [
        ('village', 'Village / Neighbourhood'),
        ('landmark', 'Landmark / Popular Place'),
    ]
    
    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_location_type_display()})"


class Property(models.Model):
    PROPERTY_TYPES = [
        ('rent', 'Monthly Rent'),
        ('lease', 'Long-term Lease'),
        ('airbnb', 'Short-stay / Airbnb'),
        ('conference', 'Conference Facility'),
    ]
    HOUSE_TYPES = [
        ('bedsitter', 'Bedsitter'),
        ('1br', '1 Bedroom'),
        ('2br', '2 Bedroom'),
        ('3br', '3 Bedroom'),
        ('4br', '4+ Bedroom'),
    ]
    ELECTRICITY_CHOICES = [
        ('separate', 'Separate bill'),
        ('included', 'Included in rent'),
        ('solar', 'Solar only'),
    ]
    WATER_SOURCE_CHOICES = [
        ('county', 'County supply'),
        ('borehole', 'Borehole'),
        ('tank', 'Raised tank'),
        ('truck', 'Water truck'),
    ]
    CAPACITY_RANGES = [
        ('0_20', 'Up to 20 people'),
        ('20_30', '20 - 30 people'),
        ('30_50', '30 - 50 people'),
        ('50_100', '50 - 100 people'),
        ('100_plus', '100+ people'),
    ]
    LISTING_TIERS = [
        ('free', 'Free'),
        ('standard', 'Standard - KES 100/month'),
        ('featured', 'Featured - KES 300/month'),
        ('premium', 'Premium - KES 500/month'),
    ]

    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='rent')
    view_count = models.PositiveIntegerField(default=0)

    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    location_neighbourhood = models.CharField(max_length=100, blank=True)
    location_landmark = models.CharField(max_length=200, blank=True)

    is_in_compound = models.BooleanField(default=False)
    compound_name = models.CharField(max_length=100, blank=True)
    total_units_in_compound = models.PositiveSmallIntegerField(null=True, blank=True)
    total_units = models.PositiveSmallIntegerField(default=1)
    unit_number = models.CharField(max_length=10, blank=True)

    monthly_rent = models.PositiveIntegerField(null=True, blank=True)
    deposit = models.PositiveIntegerField(null=True, blank=True)
    min_lease_months = models.PositiveSmallIntegerField(default=6)
    is_furnished = models.BooleanField(default=False)

    house_type = models.CharField(max_length=20, choices=HOUSE_TYPES, blank=True)
    has_tiles = models.BooleanField(default=False)
    has_terrazzo = models.BooleanField(default=False)
    has_water = models.BooleanField(default=False)
    water_source = models.CharField(max_length=20, choices=WATER_SOURCE_CHOICES, blank=True)
    water_schedule = models.CharField(max_length=150, blank=True)
    has_hot_shower = models.BooleanField(default=False)
    has_internet = models.BooleanField(default=False)
    parking_capacity = models.PositiveSmallIntegerField(default=0)
    electricity_billing = models.CharField(max_length=20, choices=ELECTRICITY_CHOICES, default='separate')
    has_shop_room = models.BooleanField(default=False)
    extra_features = models.TextField(blank=True)

    nightly_rate = models.PositiveIntegerField(null=True, blank=True)
    cleaning_fee = models.PositiveIntegerField(default=0)
    min_nights = models.PositiveSmallIntegerField(default=1)
    max_guests = models.PositiveSmallIntegerField(null=True, blank=True)
    bedrooms = models.PositiveSmallIntegerField(default=1)
    beds = models.PositiveSmallIntegerField(default=1)
    baths = models.DecimalField(max_digits=2, decimal_places=1, default=1.0)
    has_kitchen = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    blocked_dates = models.TextField(blank=True)

    capacity = models.PositiveSmallIntegerField(null=True, blank=True)
    capacity_range = models.CharField(max_length=20, choices=CAPACITY_RANGES, blank=True)
    hourly_rate = models.PositiveIntegerField(null=True, blank=True)
    half_day_rate = models.PositiveIntegerField(null=True, blank=True)
    full_day_rate = models.PositiveIntegerField(null=True, blank=True)
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=False)
    has_sound_system = models.BooleanField(default=False)
    catering_available = models.BooleanField(default=False)
    conference_notes = models.TextField(blank=True)

    image1 = models.ImageField(upload_to='manyumbavacant/', blank=True)
    image2 = models.ImageField(upload_to='manyumbavacant/', blank=True)
    image3 = models.ImageField(upload_to='manyumbavacant/', blank=True)
    image4 = models.ImageField(upload_to='manyumbavacant/', blank=True)

    listing_tier = models.CharField(max_length=20, choices=LISTING_TIERS, default='free')
    tier_expiry = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    payment_confirmed = models.BooleanField(default=False)
    promotion_start = models.DateTimeField(null=True, blank=True)
    total_paid = models.PositiveIntegerField(default=0)

    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    flag_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.property_type in ['rent', 'lease']:
            return f"{self.title} - KES {self.monthly_rent}/month"
        elif self.property_type == 'airbnb':
            return f"{self.title} - KES {self.nightly_rate}/night"
        else:
            return f"{self.title} - Conference"


class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    PAYMENT_TIERS = [
        ('standard', 'Standard - KES 100'),
        ('featured', 'Featured - KES 300'),
        ('premium', 'Premium - KES 500'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='payments')
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='payments')
    tier = models.CharField(max_length=20, choices=PAYMENT_TIERS)
    amount = models.PositiveIntegerField()
    transaction_id = models.CharField(max_length=100, unique=True)
    mpesa_receipt = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.property.title} - {self.tier} - {self.status}"


class Advertiser(models.Model):
    business_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


class Advertisement(models.Model):
    POSITION_CHOICES = [
        ('global', 'Global - All pages'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
        ('between_listings', 'Between listings'),
        ('property_sidebar', 'Property sidebar'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]

    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='ads/', blank=True)
    link_url = models.URLField()
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='sidebar')
    display_order = models.PositiveSmallIntegerField(default=0)
    amount_paid = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    clicks = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.position})"


class Report(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reports')
    reporter_ip = models.GenericIPAddressField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    resolution_note = models.TextField(blank=True)

    def __str__(self):
        return f"Report on {self.property.title}"
