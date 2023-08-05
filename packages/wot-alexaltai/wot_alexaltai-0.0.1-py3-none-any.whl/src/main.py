from app import ammos, armours, guns
# from app import cool_armour


if __name__ == '__main__':
    gun = guns.Gun(120, 40)
    HEAT_ammo = ammos.HEATCartridge(gun)
    armour = armours.HArmour(120)

    print(HEAT_ammo.get_demage())