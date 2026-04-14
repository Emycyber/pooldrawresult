from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.country})"


class Week(models.Model):
    number = models.IntegerField()
    season = models.CharField(max_length=20)
    date = models.DateField(help_text="The Saturday this week's matches are played")

    class Meta:
        ordering = ['-number']

    def __str__(self):
        return f"Week {self.number} ({self.season})"


class Match(models.Model):
    STATUS_CHOICES = [
        ('fixture', 'Fixture'),
        ('live', 'Live'),
        ('result', 'Result'),
        ('postponed', 'Postponed'),
        ('void', 'Void'),
    ]

    PREDICTION_CHOICES = [
        ('1', 'Home'),
        ('X', 'Draw'),
        ('2', 'Away'),
    ]

    DAY_CHOICES = [
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('EKO', 'EKO - Early Kick Off'),
        ('LKO', 'LKO - Late Kick Off'),
    ]

    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='matches')
    match_number = models.PositiveIntegerField()
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True)
    day = models.CharField(max_length=10, choices=DAY_CHOICES, blank=True)  # ← replaces date

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')

    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='fixture')
    prediction = models.CharField(max_length=1, choices=PREDICTION_CHOICES, blank=True)

    class Meta:
        ordering = ['match_number']
        unique_together = ['week', 'match_number']

    def __str__(self):
        return f"[{self.week}] {self.match_number}. {self.home_team} vs {self.away_team}"

    @property
    def is_draw(self):
        return (
            self.status == 'result' and
            self.home_score is not None and
            self.away_score is not None and
            self.home_score == self.away_score
        )

    @property
    def result(self):
        if self.home_score is not None and self.away_score is not None:
            return f"{self.home_score} – {self.away_score}"
        return "–"
    
    
class FooterLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    opens_in_new_tab = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title