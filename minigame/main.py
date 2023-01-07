from Classes import *
from subprocess import run
from random import randint
from time import sleep

# pygame used only for music
from pygame import mixer

mixer.init()
mixer.music.set_volume(0.5)


def play_music(path, skip=0):
    mixer.music.load(path)
    mixer.music.play(start=skip)


def stop_music():
    mixer.music.stop()


global hero

game = True

transishn = 0.5

global system
system = "clear"
global cheats
cheats = False

global turn
turn = 0


def settings():
    with open("data/settings.txt", "r") as file:
        global system
        global transishn
        global cheats
        gt = file.read().split("\n")
        if gt[0].split(":")[1] == " Linux" or gt[0].split(":")[1] == " Mac":
            system = "clear"
        elif gt[0].split(":")[1] == " Windows":
            system = "cls"
        transishn = float(gt[1].split(":")[1][1::])
        cheats = bool(int(gt[2].split(":")[1][1:]))
    print("\n\n\n\nZoom in\n"
          "Strip should take screen width\n"
          "Press anything when ready\n" + "---" * 30)


# def set_transition():
#     global transishn
#     print("Set animation time (default = 0.5)\n"
#           "1 - Default (0.5s)\n"
#           "2 - Short (0.35s)\n"
#           "3 - Ultra short(0.2s)")
#     while True:
#         trans = input()
#         match trans:
#             case "1":
#                 transishn = 0.5
#             case "2":
#                 transishn = 0.35
#             case "3":
#                 transishn = 0.2
#             case _:
#                 print("Try again")
#                 continue
#         break


# supporting
def clear():
    global system
    run(system, shell=True)


def is_enough(price):
    global hero
    if hero.souls < price:
        print("Not enough souls")
    return hero.souls >= price


def counter():
    count = 0

    def inner(key="w", st=0):
        nonlocal count
        match key:
            case "w":
                count += 1
            case "r":
                return count
            case "reset":
                count = 0
            case "set":
                count += st

    return inner


# counters
village = counter()
dungeon = counter()
swamp = counter()
kingdom = counter()

fight_counter = counter()


def save():
    global hero
    with open("save.txt", "w") as file:
        file.write(
            f"{hero.name} {hero.max_hp} {hero.souls} {hero.agility} {hero.strength} {hero.weapon.weapon_type + 's'} {(''.join(hero.weapon.name.split())).lower()}\n")
        file.write(f"{village('r')}\n"
                   f"{dungeon('r')}\n"
                   f"{swamp('r')}\n"
                   f"{kingdom('r')}\n"
                   f"{fight_counter('r')}\n")

        # Load


def start():
    clear()
    global hero
    print("Terminal Souls\n")
    print("Enter heroes name:")
    while True:
        hero_name = input()
        if hero_name.isdigit():
            print("Normal name")
            continue
        break
    print("Choose your starter class:\n"
          "1 - swordsman\n"
          "2 - bandit\n"
          "3 - paladin\n\n"
          "4 - ~load my save~")
    while True:
        choice = input()
        match choice:
            case "1":
                hero = Hero(hero_name, 460, 0, 6, 6, weapons_data["swords"]["shortsword"])
            case "2":
                hero = Hero(hero_name, 420, 0, 9, 2, weapons_data["daggers"]["knife"])
            case "3":
                hero = Hero(hero_name, 500, 0, 3, 7, weapons_data["hummers"]["club"])
            case "4":
                with open("save.txt", "r") as file:
                    xx = file.read().split("\n")
                    x = xx[0]
                    print(x)
                    if len(x) <= 10:
                        print("No saves")
                        continue
                    else:
                        x = x.split()
                        i = str(x[6])
                        while "+" in i:
                            i = i.replace("+", "")
                        hero = Hero(str(x[0]), int(x[1]), float(x[2]), int(x[3]), int(x[4]),
                                    weapons_data[str(x[5])][i])
                        if "+" in str(x[6]):
                            hero.weapon.upgrade()
                        if "++" in str(x[6]):
                            hero.weapon.advanced_upgrade()
                    village("set", int(xx[1]))
                    dungeon("set", int(xx[2]))
                    swamp("set", int(xx[3]))
                    kingdom("set", int(xx[4]))

                    fight_counter("set", int(xx[5]))

            case _:
                print("Try again")
                continue
        break


def idle():
    global hero
    clear()
    hero.show_main(["lvl", "max_hp", "weapon", "_Hero__damage"])
    print("1 - visit shop\n"
          "2 - lvl up\n"
          "3 - check bag\n"
          "4 - show current weapon stats\n"
          "5 - explore locations\n\n"
          "6 - save")
    while True:
        choice = input()
        if choice in tuple("123456") or choice == "228" or choice == "337":
            return int(choice)
        print("Try again")


# 1 action
def shop():
    global hero
    clear()
    hero.show_main()
    print("Shop:\n"
          "1 - Long sword    (2700 souls)\n"
          "2 - Bandit dagger (2300 souls)\n"
          "3 - Mace          (3200 souls)\n")
    if fight_counter('r') > 35:
        print("4 - grindstone I  (5500 souls)\n"
              "        ~upgrade your equipped weapon~\n\n"
              "5 - bonfire ascetic (8320 souls)\n"
              "        ~reload location~\n\n"
              "6 - Enchanted long sword  (16000 souls)\n"
              "7 - Cursed curved sword   (18000 souls)\n"
              "8 - Demons mace           (21000 souls)\n\n"
              "9 - grindstone II  (32000 souls)\n"
              "        ~upgrade your equipped weapon~\n")
    elif fight_counter('r') > 15:
        print("4 - grindstone I  (5500 souls)\n"
              "        ~upgrade your equipped weapon~\n\n"
              "5 - bonfire ascetic (8320 souls)\n"
              "        ~reload location~\n")
    print("Q - ~Exit~")

    while True:
        purchase = None
        choice = input()
        match choice:
            case "1":
                price = 2300
                if not is_enough(price):
                    continue
                purchase = weapons_data["swords"]["longsword"]
            case "2":
                price = 2100
                if not is_enough(price):
                    continue
                purchase = weapons_data["daggers"]["banditdagger"]
            case "3":
                price = 3200
                if not is_enough(price):
                    continue
                purchase = weapons_data["hummers"]["mace"]
            case "4":
                price = 5500
                if not is_enough(price):
                    continue
                if "+" in hero.weapon.name:
                    print("Weapon already upgraded")
                    continue
                hero.weapon.upgrade()
                hero.reset_damage()
            case "5":
                price = 8320
                if not is_enough(price):
                    continue
                print("Bofire ascetic\n"
                      "Choose location to reload:\n"
                      f"1 - Undead village ({13 - village('r')})\n"
                      f"2 - Dungeon ({13 - dungeon('r')})\n"
                      f"3 - Cursed swamp ({13 - swamp('r')})\n"
                      f"4 - Kingdom ({13 - kingdom('r')})\n")
                while True:
                    x = input()
                    match x:
                        case "1":
                            village("reset")
                        case "2":
                            dungeon("reset")
                        case "3":
                            swamp("reset")
                        case "4":
                            kingdom("reset")
                        case _:
                            print("Try again")
                            continue
                    break
            case "6":
                price = 16000
                if not is_enough(price):
                    continue
                purchase = weapons_data["swords"]["enchantedlongsword"]
            case "7":
                price = 18000
                if not is_enough(price):
                    continue
                purchase = weapons_data["daggers"]["cursedcurvedsword"]
            case "8":
                price = 21000
                if not is_enough(price):
                    continue
                purchase = weapons_data["hummers"]["demonsmace"]
            case "9":
                price = 32000
                if not is_enough(price):
                    continue
                if not ("+" in hero.weapon.name):
                    print("Weapon is too weak")
                    continue
                if "++" in hero.weapon.name:
                    print("Weapon is already upgraded")
                    continue
                hero.weapon.advanced_upgrade()
                hero.reset_damage()
            case "q":
                break
            case _:
                print("Try again")
                continue
        hero.spend_souls(price)
        if purchase:
            hero.get_item(purchase)
        break


# 2 action
def lvl_up():
    manual = [" ", " ", " "]
    global hero
    while True:
        clear()
        hero.show_main(["lvl", "max_hp", "damage_block", "agility", "strength"])
        print(f"Level up "
              f"(Required - {hero.lvl_price} souls):\n\n"
              f"1 - Vitality   {manual[0]}\n"
              f"2 - Agility    {manual[1]}\n"
              f"3 - Strength   {manual[2]}\n"
              f"4 - ~Open Manual~\n"
              "Q - ~Exit~")
        choice = input()
        if choice in tuple("123"):
            if not is_enough(hero.lvl_price):
                continue
            hero.lvl_up(int(choice))
            break
        elif choice == "4":
            manual = [
                "+40 health, +5 health regen",
                "+1 agility, +0.5% dodge chance, +0.3% prick chance, +2 prick damage",
                "+1 strength +0.5% block, +6 heavy attack damage"
            ]
            clear()

        elif choice == "q":
            break
        else:
            print("Try again")


# 3 action
def check_bag():
    global hero
    clear()
    hero.show_main(["weapon"])
    hero.show_bag()
    while True:
        choice = input()
        if choice.isdigit():
            choice = int(choice)
            if choice <= len(hero.bag) and (choice >= 1):
                hero.obtain_weapon(hero.bag[choice - 1])
                break
            else:
                print("Try again")
        else:
            print("Try again")

        # 4 action


def check_weapon():
    global hero
    clear()
    hero.show_main()
    hero.weapon.show_stats()
    input("Press any button\n")


# 5 action
def fight():
    global hero
    global game
    enemy: Enemy = choose_enemy()
    hero.health = hero.max_hp
    enemy.health = enemy.max_health
    while enemy.health > 0:
        if hero.health <= 0:
            stop_music()
            clear()
            print("Party is over")
            mixer.music.set_volume(1)
            play_music("Music/Death.mp3", 0.2)
            input("~Press anything~")
            stop_music()
            return False
        show_status(enemy)
        choose_action(enemy, transishn)
    else:
        stop_music()
        hero.souls += enemy.souls * (1 + 0.2 * int(hero.health == hero.max_hp))
        if enemy.end is False:
            clear()
            print("Congrat\n"
                  "Demon vanquished\n"
                  "----------------")
            play_music("Music/Victory.mp3", )
            hero.show_main(["lvl", "weapon"])
            input("~Press anything~")
            stop_music()
        return enemy.end


def show_status(enemy: Enemy):
    global hero
    space_range = 25 - (len(enemy.name_s) - len(enemy.name))
    range_for_hp = 25 - (len(str(round(hero.health, 1)) + str(hero.max_hp)) + 3 - len(hero.name)) - (
            len(str(round(enemy.health, 1)) + str(enemy.max_health)) + 3 - len(enemy.name))
    clear()
    print(f"{hero.name} {' ' * space_range} {enemy.name_s}\n"
          f"{hero.health:.1f}/{hero.max_hp} {' ' * range_for_hp} {enemy.health:.1f}/{enemy.max_health}")


def choose_action(enemy: Enemy, transition=0.5):
    global hero
    action = hero.swords_skills()
    clear()
    show_status(enemy)
    sleep(transition)
    enemy.health -= action[0]
    take_damage_animaton(enemy, enemy)
    if enemy.health <= 0:
        sleep(transition)
        return 0
    for i in range(action[1]):
        sleep(transition)
        enemy.fight_back(hero, action[2], action[3])
        take_damage_animaton(enemy, hero)
        if hero.health <= 0:
            sleep(transition)
            return 0
    sleep(transition)


def take_damage_animaton(enemy: Enemy, target):
    global hero
    space_range = 25 - (len(enemy.name_s) - len(enemy.name))
    range_for_hp = 25 - (len(str(round(hero.health, 1)) + str(hero.max_hp)) + 3 - len(hero.name)) - (
            len(str(round(enemy.health, 1)) + str(enemy.max_health)) + 3 - len(enemy.name))
    clear()
    if target == hero:
        print(f"{hero.name} {' ' * space_range} {enemy.name_s}\n"
              f"- {hero.health:.1f}/{hero.max_hp} - {' ' * (range_for_hp - 4)} {enemy.health:.1f}/{enemy.max_health}")
    elif target == enemy:
        print(f"{hero.name} {' ' * space_range} {enemy.name_s}\n"
              f"{hero.health:.1f}/{hero.max_hp} {' ' * (range_for_hp - 4)} - {enemy.health:.1f}/{enemy.max_health} -")


global stage_couter
stage_couter = 12


def choose_enemy():
    clear()
    hero.show_main(["lvl"])
    print("Choose way:             recommended:\n"
          f"1 - Undead village          10+ ({'Boss' if village('r') == stage_couter else ('closed' if village('r') > stage_couter else stage_couter - village('r'))})\n" +
          f"2 - Dungeon                 15+ ({'Boss' if dungeon('r') == stage_couter else ('closed' if dungeon('r') > stage_couter else stage_couter - dungeon('r'))})" * int(
        fight_counter('r') > 10) + "\n" +
          f"3 - Cursed swamp            21+ ({'Boss' if swamp('r') == stage_couter else ('closed' if swamp('r') > stage_couter else stage_couter - swamp('r'))})" * int(
        fight_counter('r') > 20) + "\n" +
          f"4 - Kingdom                 36+ ({'Boss' if kingdom('r') == stage_couter else ('closed' if kingdom('r') > stage_couter else stage_couter - kingdom('r'))})" * int(
        fight_counter('r') > 30) + "\n" +
          "5 - Boss                    48+" * int(fight_counter('r') > 42))
    while True:
        choice = input()
        current = None
        match choice:
            case "1":
                if village("r") > stage_couter:
                    print("closed")
                    continue
                choice = "village"
                village()
                current = village('r')
                skeep = 106
            case "2":
                if fight_counter('r') <= 10 or dungeon("r") > stage_couter:
                    print("closed")
                    continue
                choice = "dungeon"
                dungeon()
                current = dungeon('r')
                skeep = 64
            case "3":
                if fight_counter('r') <= 20 or swamp("r") > stage_couter:
                    print("closed")
                    continue
                choice = "swamp"
                swamp()
                current = swamp('r')
                skeep = 127
            case "4":
                if fight_counter('r') <= 30 or kingdom("r") > stage_couter:
                    print("closed")
                    continue
                choice = "kingdom"
                kingdom()
                current = kingdom('r')
                skeep = 0
            case "5":
                if fight_counter('r') <= 42:
                    print("closed")
                choice = "boss"
                current = 13
                skeep = 0
            case _:
                print("Try again")
                continue
        fight_counter()
        if current == stage_couter + 1:
            x = len(enemies_data[choice])
            play_music(f"MiniBoss/Miniboss{choice}.mp3", skeep)
            return enemies_data[choice][len(enemies_data[choice]) - 1]
        else:
            x = len(enemies_data[choice])
            return enemies_data[choice][randint(0, x - 2)]


# 228 action
def get_souls():
    print(cheats)
    x = 0
    global hero
    if cheats:
        x = 6000
    hero.souls += x


def unlock():
    x = 'r'
    if cheats:
        fight_counter("set", 60)
    else:
        pass
