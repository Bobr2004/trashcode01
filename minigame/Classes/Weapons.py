class Weapon:
    def __init__(self, name: str, weapon_type, base_dmg: int, ag_scale: str, st_scale: str):
        self.name = name
        self.weapon_type = weapon_type
        self.base_damage = base_dmg
        self.agility_scale = ag_scale
        self.strength_scale = st_scale

    def show_stats(self, underline: bool = False):
        for attr, value in self.__dict__.items():
            if attr == "name":
                print(f"{value}")
                continue
            print(f"{attr.title()} - {value}")
        print("---" * (5 * int(underline)))

    def upgrade(self):
        self.name = self.name + "+"
        self.base_damage += 40
        self.agility_scale = self.upgrade_scales(self.agility_scale)
        self.strength_scale = self.upgrade_scales(self.strength_scale)

    def advanced_upgrade(self):
        self.name = self.name + "+"
        self.base_damage += 50
        self.agility_scale = self.upgrade_scales(self.agility_scale)
        self.strength_scale = self.upgrade_scales(self.strength_scale)

    def upgrade_scales(self, scale):
        match scale:
            case "-":
                return "F"
            case "F":
                return "E"
            case "E":
                return "D"
            case "D":
                return "C"
            case "C":
                return "B"
            case "B":
                return "A"
            case "A":
                return "S"
            case "S":
                return "SS"
            case "SS":
                return "SSS"


weapons_data = {
    "swords": {
        "shortsword": Weapon("Short sword", "sword", 68, "C", "D"),
        "longsword": Weapon("Long sword", "sword", 100, "B", "B"),
        "enchantedlongsword": Weapon("Enchanted long sword", "sword", 150, "A", "B")
    },
    "daggers": {
        "knife": Weapon("Knife", "dagger", 55, "B", "F"),
        "banditdagger": Weapon("Bandit dagger", "dagger", 90, "A", "E"),
        "cursedcurvedsword": Weapon("Cursed curved sword", "dagger", 130, "S", "D")

    },
    "hummers": {
        "club": Weapon("Club", "hummer", 75, "F", "B"),
        "mace": Weapon("Mace", "hummer", 115, "E", "B"),
        "demonsmace": Weapon("Demon mace", "hummer", 130, "D", "S")
    }
}
