from django.db import models


class Agent(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class PolicyHolder(models.Model):

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    policy_number = models.CharField(max_length=50, unique=True)

    holder_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)  # NEW EMAIL FIELD

    total_amount = models.IntegerField()

    start_date = models.DateField()

    policy_years = models.IntegerField()

    maturity_date = models.DateField(null=True, blank=True)

    PAYMENT_CHOICES = [
        (1, "Monthly"),
        (3, "3 Months"),
        (6, "6 Months"),
        (12, "1 Year"),
    ]

    payment_interval = models.IntegerField(choices=PAYMENT_CHOICES)

    next_due_date = models.DateField()

    def __str__(self):
        return f"{self.policy_number} - {self.holder_name}"