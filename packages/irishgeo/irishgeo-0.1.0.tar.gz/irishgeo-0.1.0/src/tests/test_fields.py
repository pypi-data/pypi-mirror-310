from django.core.exceptions import ValidationError
from irishgeo.fields import IrishStateField, IrishEircodeField, validate_eircode

# Test Irish Eircode validation
def test_valid_eircode():
    validate_eircode("A65 F4E2")  # Should not raise ValidationError

def test_invalid_eircode():
    try:
        validate_eircode("INVALID")
    except ValidationError as e:
        assert str(e) == "['INVALID is not a valid Eircode.']"

# Test Irish State Field choices
def test_irish_state_field_choices():
    field = IrishStateField()
    assert ("D", "Dublin") in field.choices

