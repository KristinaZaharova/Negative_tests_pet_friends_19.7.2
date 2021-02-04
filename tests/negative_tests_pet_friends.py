from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_wrong_email(email='bjhbhbj', password=valid_password):
    """Проверяем что запрос api ключа c неверной почтой не выполнится"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_wrong_filter(filter='opmm'):
    """Проверяем что запрос всех питомцев c неверным фильтром не выполнится"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_wrong_key(filter=''):
    """Проверяем что запрос всех питомцев без ключа не выполнится"""
    status, result = pf.get_list_of_pets("auth_key", filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_api_pets_no_name(animal_type='dog', age='2', pet_photo='animals.jpg'):
    """Проверяем что нельзя добавить питомца без имени"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_api_pets(auth_key, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age

def test_post_api_pets_no_photo(name='dog', animal_type='dog', age='3', pet_photo=''):
    """Проверяем что нельзя добавить питомца с пустым фото"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pets_no_id():
    """Проверяем что нельзя удалить питомца без id"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_api_pets(auth_key, "dog", "dog", "2", "animals.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status,_ = pf.delete_pet(auth_key)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_pets_wrong_password():
    """Проверяем что нельзя удалить питомца c неверным паролем"""
    _, auth_key = pf.get_api_key(valid_email, "123456")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_api_pets(auth_key, "dog", "dog", "2", "animals.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status,_ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_put_pet_no_id(name='милашка', animal_type='панда', age=3):
    """Проверяем что нельзя изменить питомца без id"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.put_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_put_pet_no_age(name='милашка', animal_type='панда'):
    """Проверяем что нельзя изменить питомца без возраста"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.put_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_put_pet_no_type(name='милашка', age=3):
    """Проверяем что нельзя изменить питомца без типа животного"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.put_pet(auth_key, my_pets['pets'][0]['id'], name, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

