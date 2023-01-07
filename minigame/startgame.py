from main import *

if __name__ == "__main__":
    stop_music()
    global turn
    settings()
    input()
    start()
    while game:
        turn += 1
        choice = idle()
        match choice:
            case 1:
                shop()
            case 2:
                lvl_up()
            case 3:
                check_bag()
            case 4:
                check_weapon()
            case 5:
                game = fight()
            case 228:
                get_souls()
            case 337:
                unlock()
            case 6:
                save()
    print(f"{turn} turns")
    stop_music()
