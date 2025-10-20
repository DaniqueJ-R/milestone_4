from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (0, '(0) Appalling'),
        (1, '(1) Very Bad'),
        (2, '(2) Bad'),
        (3, '(3) Average'),
        (4, '(4) Very Good'),
        (5, '(5) Amazing'),
    ]

    star_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Star Rating'
    )

    class Meta:
        model = Review
        fields = ['review_title', 'review_body', 'star_rating']
        widgets = {
            'review_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Required..',
            }),
            'review_body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a review here...',
                'rows': 5,
            }),
        }
        labels = {
            'review_title': 'Review Title:',
            'review_body': 'Review',
        }
