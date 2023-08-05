# Haptik Helpers

*Library of Helpers function to be re-used in Haptic Code nodes*

### Installation

```
pip install haptik-helpers
```

### Get started
How to Find Entity in Haptik conversation entity object(dict):

```Python
from haptik_helpers import Integrations

# Instantiate a Integrations object
integrate = Integrations(entity_obj)

# Call the get_entity method
print(integrate.get_entity("kli_otp"))
```