
class Integrations:
    """
    Instantiate a Integration Class.
    Entities Provided in constructor will be used for further operations.
    
    :param entities: List of Haptik Entities.
    :type entities: dict
    """
    def __init__(self, entities):
        self.entities = entities

    def get_entity(self, key, default='') -> str:
        """
        Searches for given key in entity and returns `original_text` for the same.
        
        :param key: key to serach in entity list.
        :type key: str

        :param default: if key is not found in entity list, this value will be send instead of None, defaults to ''.
        :type default: str, optional

        :return: original_text of given entity.
        :rtype: str
        """
        key, secondary_key, statement, *_ = key.split("|") + ["", ""]
        entity = self.entities.get(key)
        if entity:
            entity_value = entity[0].get('entity_value', default)
            if isinstance(entity_value, dict):
                if secondary_key in entity_value:
                    entity_value = entity_value.get(secondary_key, default)
                elif 'value' in entity_value:
                    entity_value = entity_value['value']
                else:
                    entity_value = entity[0]['original_text']
            return statement + entity_value if isinstance(entity_value, str) else entity_value
        return ''