from django.test import TestCase

# Create your tests here.
class TestThisThing:
    def test_one(self):
        x = "Some string with spaces"
        assert ' ' in x