from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from Vampires_vs_Werewolves.common.models import UserHiding
from Vampires_vs_Werewolves.profiles.models import (Sword, Shield, Boots, PowerPotion,
                                                    DefencePotion, SpeedPotion, HealthPotion)


class SwordModelTest(TestCase):
    def test_sell_price_calculation(self):
        sword = Sword(name='Test Sword', price=100)
        sword.save()
        self.assertEqual(sword.sell_price, 60)

    def test_string_representation(self):
        sword = Sword(name='Test Sword')
        self.assertEqual(str(sword), 'Test Sword')


class ShieldModelTest(TestCase):
    def test_sell_price_calculation(self):
        shield = Shield(name='Test Shield', price=120)
        shield.save()
        self.assertEqual(shield.sell_price, 72)

    def test_string_representation(self):
        shield = Shield(name='Test Shield')
        self.assertEqual(str(shield), 'Test Shield')


class BootsModelTest(TestCase):
    def test_sell_price_calculation(self):
        boots = Boots(name='Test Boots', price=90)
        boots.save()
        self.assertEqual(boots.sell_price, 54)

    def test_string_representation(self):
        boots = Boots(name='Test Boots')
        self.assertEqual(str(boots), 'Test Boots')


class PotionModelTest(TestCase):
    def test_price_calculation(self):
        power_potion = PowerPotion(percent_bonus=15, hours_active=3)
        power_potion.save()
        self.assertEqual(power_potion.price, 90)

        health_potion = HealthPotion(percent_bonus=20)
        health_potion.save()
        self.assertEqual(health_potion.price, 40)

    def test_string_representation(self):
        power_potion = PowerPotion()
        self.assertEqual(str(power_potion), 'Power')


class UserHidingModelTest(TestCase):
    def test_can_stop_hiding_calculation(self):
        hiding = UserHiding(hidden_at=timezone.now())
        hiding.save()
        expected_can_stop_hiding_at = hiding.hidden_at + timedelta(hours=12)
        self.assertEqual(hiding.can_stop_hiding_at, expected_can_stop_hiding_at)

    def test_string_representation(self):
        hiding = UserHiding()
        self.assertIn('UserHiding', str(hiding))
