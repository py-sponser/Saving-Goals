from rest_framework.serializers import ModelSerializer, DateField
from core.models import SavingGoal
from django.utils import timezone


class SavingGoalsGetterSerializer(ModelSerializer):
    date = DateField(format="%B %Y")
    current_date = DateField(format="%B %Y")

    class Meta:
        model = SavingGoal
        exclude = ("user", )


class SavingsSerializer(ModelSerializer):

    class Meta:
        model = SavingGoal
        exclude = ("user", "monthly_deposit_amount", )

    def create(self, validated_data):
        user = self.context.get("user")
        total_amount = validated_data.get("total_amount")
        target_date = validated_data.get("date")
        current_date = timezone.now()
        new_saving_goal = SavingGoal.objects.create(user=user, total_amount=total_amount, date=target_date,
                                                    current_date=current_date)
        new_saving_goal.calculate_monthly_deposit_amount(target_date, current_date, total_amount)
        new_saving_goal.save()
        return new_saving_goal
