
from imp import reload
import time
# from app import guns
# from app import ammos
# from app.armours import HArmour, SArmour
# from app.ammos import HECartridge, APCartridge, HEATCartridge

# class Tank:
#     def __init__(self, model: str, gun: guns.Gun, health: int, ammos: ammos) -> None:
#         self.model = model
#         self.gun = gun
#         self.health = health
    
#     def _add_armors(self, armours: list(HArmour, SArmour)):
#         self.armors = armours

#     def _load_ammo(self, ):
#         pass

    
def is_gun_loaded(ammo: bool, reload):
        
        if ammo == True:
            print('Пушка заряженна')
        if ammo == False:
            print(f'Пушка не заряженна\nПроизводим зарядку на {reload} секунд')
            time.sleep (reload)
            print('Перезарядка прошла успешна')
            return True

            
                
if __name__ == '__main__':
    is_gun_loaded(False, 7)
        
