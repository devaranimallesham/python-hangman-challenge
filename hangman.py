"""
=======================================================================
 ADVANCED HANGMAN  -  100% Pure Python (no files, no APIs, no internet)
=======================================================================
 Features
   * Login / Signup (kept in memory, pure Python dictionaries)
   * Main menu: Play, Themes, Levels, Statistics, How to Play, Logout
   * 36 themes with predefined words + helpful hints
   * 10 main levels (Beginner -> Legend), each with 10 sub-levels
   * 6 wrong chances per word, ASCII hangman drawn step by step
   * Limited hints (cost score), A-Z letter board, keyboard input
   * Scoring, bonus points, best score, wins/losses, achievements
   * Progressive unlocking of sub-levels and main levels
   * Game modes: Classic, Survival, Random Theme, Challenge
 Run:  python hangman.py
=======================================================================
"""

import random
import string

# ----------------------------------------------------------------------
# 1. COLORS  (simple ANSI escape codes - pure Python, no libraries)
# ----------------------------------------------------------------------


class C:
    """Small colour helper so the game looks colourful in the terminal."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GREY = "\033[90m"


def paint(text, color):
    """Return text wrapped in a colour."""
    return f"{color}{text}{C.RESET}"


def title(text):
    """Print a nice framed title bar."""
    line = "=" * 62
    print(paint(line, C.CYAN))
    print(paint(text.center(62), C.BOLD + C.YELLOW))
    print(paint(line, C.CYAN))


def rule():
    print(paint("-" * 62, C.GREY))


# ----------------------------------------------------------------------
# 2. THEMES:  36 themes, each a list of (WORD, HINT) pairs
# ----------------------------------------------------------------------

THEMES = {
    "Games": [
        ("CHESS", "Board game with kings and pawns"),
        ("TETRIS", "Falling blocks puzzle classic"),
        ("PUBG", "Battle royale on an island"),
        ("MINECRAFT", "Build anything out of blocks"),
        ("FORTNITE", "Battle royale famous for building walls"),
        ("PACMAN", "Yellow circle eating dots in a maze"),
        ("ROBLOX", "Platform full of user made games"),
        ("VALORANT", "Tactical shooter with agents"),
        ("SUDOKU", "Number puzzle in a nine by nine grid"),
        ("CANDYCRUSH", "Match three sweets on a mobile phone"),
    ],
    "Movies": [
        ("AVATAR", "Blue people on planet Pandora"),
        ("TITANIC", "Ship that met an iceberg"),
        ("INCEPTION", "A dream inside a dream"),
        ("FROZEN", "Snow queen sister sings Let It Go"),
        ("GLADIATOR", "Roman general turned arena fighter"),
        ("JAWS", "A giant shark terrorises a beach town"),
        ("INTERSTELLAR", "Wormhole journey to save humanity"),
        ("CASABLANCA", "Classic wartime romance in Morocco"),
        ("PARASITE", "Korean film about two very different families"),
        ("JURASSICPARK", "Theme park where dinosaurs escape"),
    ],
    "Heroes": [
        ("RAMA", "Hero of the Ramayana epic"),
        ("ROCKY", "Boxer who runs up museum steps"),
        ("NEO", "The One who bends the Matrix"),
        ("ARAGORN", "Ranger who becomes king of Gondor"),
        ("HERCULES", "Greek strongman of twelve labours"),
        ("SPARTACUS", "Slave who led a revolt against Rome"),
        ("LUKESKYWALKER", "Jedi son of a dark lord"),
        ("ACHILLES", "Greek warrior with a weak heel"),
        ("BEOWULF", "Old English hero who fights Grendel"),
        ("MULAN", "Warrior who takes her father's place in the army"),
    ],
    "Heroines": [
        ("LEIA", "Princess of Alderaan"),
        ("HERMIONE", "Brightest witch of her age"),
        ("KATNISS", "Archer in the Hunger Games"),
        ("WONDERWOMAN", "Amazon princess with a lasso"),
        ("ELIZABETHBENNET", "Heroine of Pride and Prejudice"),
        ("JOANOFARC", "French teenage saint and soldier"),
        ("XENA", "Television warrior princess"),
        ("MOANA", "Island girl who sails past the reef"),
        ("BLACKWIDOW", "Red haired spy of the Avengers"),
        ("SITA", "Wife of Rama in the Ramayana"),
    ],
    "Animals": [
        ("CAT", "Purrs and chases mice"),
        ("LION", "King of the jungle"),
        ("TIGER", "Big striped orange cat"),
        ("GIRAFFE", "Tallest animal on land"),
        ("ELEPHANT", "Huge animal with a trunk"),
        ("KANGAROO", "Hops and carries babies in a pouch"),
        ("CROCODILE", "Toothy reptile in rivers"),
        ("RHINOCEROS", "Thick skinned animal with a horn"),
        ("CHIMPANZEE", "Clever ape close to humans"),
        ("HIPPOPOTAMUS", "Heavy river animal with a huge mouth"),
    ],
    "Fruits": [
        ("FIG", "Small sweet fruit full of tiny seeds"),
        ("KIWI", "Fuzzy brown skin, green inside"),
        ("MANGO", "King of fruits in India"),
        ("BANANA", "Yellow and curved"),
        ("PAPAYA", "Orange tropical fruit with black seeds"),
        ("PINEAPPLE", "Spiky skin and a crown of leaves"),
        ("BLUEBERRY", "Tiny blue berry good for the brain"),
        ("WATERMELON", "Green outside, red and juicy inside"),
        ("POMEGRANATE", "Full of ruby red seeds"),
        ("DRAGONFRUIT", "Pink scaly skin with speckled flesh"),
    ],
    "Countries": [
        ("PERU", "South American home of Machu Picchu"),
        ("INDIA", "Land of the Taj Mahal"),
        ("JAPAN", "Land of the rising sun"),
        ("BRAZIL", "Amazon rainforest and samba"),
        ("CANADA", "Maple leaf on its flag"),
        ("AUSTRALIA", "Continent country with kangaroos"),
        ("SWITZERLAND", "Alps, chocolate and watches"),
        ("ARGENTINA", "Tango and Lionel Messi"),
        ("NETHERLANDS", "Tulips, windmills and bicycles"),
        ("MADAGASCAR", "Big island nation with lemurs"),
    ],
    "Sports": [
        ("GOLF", "Small ball, clubs and eighteen holes"),
        ("RUGBY", "Oval ball and heavy tackles"),
        ("TENNIS", "Racket sport with love and deuce"),
        ("HOCKEY", "Played with sticks and a puck or ball"),
        ("BASEBALL", "Bat, diamond and home runs"),
        ("SWIMMING", "Racing through lanes of water"),
        ("BADMINTON", "Racket sport with a shuttlecock"),
        ("BASKETBALL", "Dribble and dunk through a hoop"),
        ("WEIGHTLIFTING", "Snatch and clean and jerk"),
        ("SKATEBOARDING", "Tricks on four small wheels"),
    ],
    "Cricket": [
        ("BAIL", "Small piece on top of the stumps"),
        ("OVER", "Six legal deliveries"),
        ("WICKET", "Three stumps and two bails"),
        ("YORKER", "Ball aimed right at the batter's toes"),
        ("BOUNCER", "Short ball flying at the head"),
        ("STUMPED", "Keeper breaks the stumps while you are out of crease"),
        ("HATTRICK", "Three wickets in three balls"),
        ("ALLROUNDER", "Player good at both bat and ball"),
        ("POWERPLAY", "Early overs with fielding restrictions"),
        ("DUCKWORTHLEWIS", "Rain rule for revised targets"),
    ],
    "Football": [
        ("GOAL", "What every striker wants"),
        ("PENALTY", "Free shot from twelve yards"),
        ("OFFSIDE", "Ahead of the last defender too soon"),
        ("DRIBBLE", "Running with the ball at your feet"),
        ("MIDFIELDER", "Player linking defence and attack"),
        ("GOALKEEPER", "Only one allowed to use hands"),
        ("FREEKICK", "Wall of players and a curling shot"),
        ("CHAMPIONSLEAGUE", "Top European club competition"),
        ("HATTRICK", "Three goals by one player"),
        ("CORNERKICK", "Restart from the flag by the goal line"),
    ],
    "Cars": [
        ("AUDI", "Four rings on the badge"),
        ("TESLA", "Electric cars named after an inventor"),
        ("TOYOTA", "Japanese maker of the Corolla"),
        ("FERRARI", "Italian prancing horse"),
        ("BUGATTI", "Maker of the Veyron hypercar"),
        ("PORSCHE", "German maker of the 911"),
        ("MERCEDES", "Three pointed star badge"),
        ("LAMBORGHINI", "Raging bull supercar brand"),
        ("ROLLSROYCE", "Luxury car with the Spirit of Ecstasy"),
        ("VOLKSWAGEN", "German for people's car"),
    ],
    "Bikes": [
        ("BMX", "Small bike for stunts and dirt tracks"),
        ("DUCATI", "Italian maker of red superbikes"),
        ("HARLEY", "Loud American cruiser brand"),
        ("YAMAHA", "Japanese brand also making musical instruments"),
        ("KAWASAKI", "Green Ninja motorcycles"),
        ("SCOOTER", "Step through bike with small wheels"),
        ("MOUNTAINBIKE", "Fat tyres for rough trails"),
        ("ROYALENFIELD", "Thumping classic motorcycle brand"),
        ("HANDLEBAR", "You steer a bike with this"),
        ("SUSPENSION", "Absorbs the bumps in the road"),
    ],
    "Technology": [
        ("WIFI", "Wireless way to reach the internet"),
        ("ROUTER", "Box that shares your internet"),
        ("LAPTOP", "Portable folding computer"),
        ("FIREWALL", "Guards a network from attacks"),
        ("BLUETOOTH", "Short range wireless named after a king"),
        ("PROCESSOR", "The brain chip of a computer"),
        ("ENCRYPTION", "Scrambles data so only keys unlock it"),
        ("CLOUDSTORAGE", "Files kept on someone else's servers"),
        ("ARTIFICIALINTELLIGENCE", "Machines that appear to think"),
        ("VIRTUALREALITY", "Headset world you can look around in"),
    ],
    "Programming": [
        ("LOOP", "Repeats a block of code"),
        ("PYTHON", "Language named after a comedy group"),
        ("STRING", "Text data type"),
        ("FUNCTION", "Reusable named block of code"),
        ("VARIABLE", "A named box that stores a value"),
        ("DICTIONARY", "Python type of key value pairs"),
        ("RECURSION", "A function that calls itself"),
        ("ALGORITHM", "Step by step recipe for solving a problem"),
        ("INHERITANCE", "One class taking features from another"),
        ("POLYMORPHISM", "Same method name, different behaviour"),
    ],
    "Food": [
        ("SOUP", "Warm liquid meal in a bowl"),
        ("PIZZA", "Round, cheesy, sliced into triangles"),
        ("BURGER", "Patty between two buns"),
        ("NOODLES", "Long strands slurped with chopsticks"),
        ("SANDWICH", "Filling between two slices of bread"),
        ("BIRYANI", "Spiced rice dish cooked in layers"),
        ("PANCAKE", "Flat breakfast disc with syrup"),
        ("CHOCOLATE", "Sweet made from cocoa"),
        ("SPAGHETTI", "Long thin Italian pasta"),
        ("CHEESECAKE", "Creamy dessert on a biscuit base"),
    ],
    "Cartoons": [
        ("TOM", "Cat who chases Jerry"),
        ("DORA", "Explorer with a map and a backpack"),
        ("POPEYE", "Sailor powered by spinach"),
        ("SPONGEBOB", "Yellow sponge in Bikini Bottom"),
        ("SCOOBYDOO", "Great Dane who solves mysteries"),
        ("PINKPANTHER", "Silent pink cartoon cat"),
        ("POWERPUFFGIRLS", "Three sisters made of sugar and spice"),
        ("SHINCHAN", "Cheeky five year old Japanese boy"),
        ("LOONEYTUNES", "That's all folks"),
        ("MICKEYMOUSE", "Mouse with round black ears"),
    ],
    "Superheroes": [
        ("THOR", "God of thunder with a hammer"),
        ("HULK", "Green and very angry"),
        ("BATMAN", "Dark knight of Gotham"),
        ("IRONMAN", "Genius in a flying metal suit"),
        ("SPIDERMAN", "Web slinger of New York"),
        ("SUPERMAN", "Kryptonian in a red cape"),
        ("AQUAMAN", "King who talks to sea creatures"),
        ("DEADPOOL", "Merc with a mouth"),
        ("BLACKPANTHER", "King of Wakanda"),
        ("DOCTORSTRANGE", "Sorcerer Supreme with a cloak"),
    ],
    "Villains": [
        ("LOKI", "Trickster brother of Thor"),
        ("JOKER", "Clown prince of crime"),
        ("THANOS", "Purple titan collecting stones"),
        ("SAURON", "Dark lord of the One Ring"),
        ("VOLDEMORT", "He who must not be named"),
        ("MAGNETO", "Mutant who controls metal"),
        ("SCARFACE", "Not a villain of comics, but of Miami crime"),
        ("DARTHVADER", "Breathing black armoured Sith"),
        ("LEXLUTHOR", "Bald billionaire enemy of Superman"),
        ("CRUELLADEVIL", "Wants a coat of dalmatian fur"),
    ],
    "TV Shows": [
        ("LOST", "Survivors on a mysterious island"),
        ("FRIENDS", "Six people and a coffee shop"),
        ("SHERLOCK", "Modern detective at Baker Street"),
        ("THEOFFICE", "Mockumentary about paper sales"),
        ("BREAKINGBAD", "Chemistry teacher turns criminal"),
        ("STRANGERTHINGS", "Upside Down in Hawkins"),
        ("GAMEOFTHRONES", "Winter is coming"),
        ("MONEYHEIST", "Red jumpsuits and Dali masks"),
        ("PEAKYBLINDERS", "Birmingham gang with razor caps"),
        ("THEMANDALORIAN", "Bounty hunter with a small green companion"),
    ],
    "Space": [
        ("MARS", "The red planet"),
        ("COMET", "Icy body with a glowing tail"),
        ("GALAXY", "Huge system of billions of stars"),
        ("NEBULA", "Cloud of gas where stars are born"),
        ("SATURN", "Planet famous for its rings"),
        ("ASTEROID", "Rocky object mostly between Mars and Jupiter"),
        ("BLACKHOLE", "Even light cannot escape it"),
        ("SUPERNOVA", "Explosive death of a massive star"),
        ("CONSTELLATION", "Pattern of stars like Orion"),
        ("INTERNATIONALSPACESTATION", "Laboratory orbiting the Earth"),
    ],
    "Nature": [
        ("LEAF", "Green part of a plant"),
        ("RIVER", "Water flowing to the sea"),
        ("FOREST", "Large area thick with trees"),
        ("GLACIER", "Slow moving river of ice"),
        ("VOLCANO", "Mountain that erupts lava"),
        ("WATERFALL", "Water dropping off a cliff"),
        ("RAINBOW", "Seven colours after the rain"),
        ("EARTHQUAKE", "The ground shakes suddenly"),
        ("PHOTOSYNTHESIS", "How plants make food from light"),
        ("BIODIVERSITY", "Variety of life in a place"),
    ],
    "Birds": [
        ("OWL", "Night bird that turns its head far"),
        ("CROW", "Clever black bird"),
        ("EAGLE", "Sharp eyed bird of prey"),
        ("PARROT", "Colourful bird that copies speech"),
        ("PENGUIN", "Bird that swims but cannot fly"),
        ("PEACOCK", "Fans out a huge colourful tail"),
        ("FLAMINGO", "Pink bird standing on one leg"),
        ("OSTRICH", "Largest bird, runs very fast"),
        ("WOODPECKER", "Drums holes into tree trunks"),
        ("HUMMINGBIRD", "Tiny bird that hovers at flowers"),
    ],
    "Famous Places": [
        ("EIFFELTOWER", "Iron tower in Paris"),
        ("TAJMAHAL", "White marble tomb in Agra"),
        ("COLOSSEUM", "Ancient arena in Rome"),
        ("STONEHENGE", "Ring of standing stones in England"),
        ("PYRAMIDS", "Ancient tombs of Egyptian kings"),
        ("GREATWALL", "Long defensive structure in China"),
        ("MACHUPICCHU", "Inca city high in the Andes"),
        ("NIAGARAFALLS", "Famous falls on a US Canada border"),
        ("SYDNEYOPERAHOUSE", "Sail shaped building in Australia"),
        ("STATUEOFLIBERTY", "Gift from France standing in a harbour"),
    ],
    "Actors": [
        ("TOMHANKS", "Played Forrest Gump"),
        ("WILLSMITH", "Fresh Prince turned movie star"),
        ("BRADPITT", "Starred in Fight Club"),
        ("JOHNNYDEPP", "Played Captain Jack Sparrow"),
        ("SHAHRUKHKHAN", "King of Bollywood"),
        ("ROBERTDOWNEYJR", "Played Iron Man"),
        ("MORGANFREEMAN", "Famous deep narrating voice"),
        ("KEANUREEVES", "Played Neo and John Wick"),
        ("LEONARDODICAPRIO", "Sank with the Titanic, later won an Oscar"),
        ("DENZELWASHINGTON", "Starred in Training Day"),
    ],
    "Athletes": [
        ("PELE", "Brazilian football legend"),
        ("MESSI", "Argentine number ten"),
        ("BOLT", "Fastest man over one hundred metres"),
        ("FEDERER", "Swiss tennis great"),
        ("RONALDO", "Portuguese star who shouts Siuu"),
        ("SERENAWILLIAMS", "Dominant American tennis champion"),
        ("MICHAELJORDAN", "Basketball icon wearing twenty three"),
        ("SACHINTENDULKAR", "Cricket's little master"),
        ("MICHAELPHELPS", "Swimmer with the most Olympic golds"),
        ("MUHAMMADALI", "Float like a butterfly, sting like a bee"),
    ],
    "Music": [
        ("DRUM", "You hit it with sticks"),
        ("PIANO", "Eighty eight black and white keys"),
        ("GUITAR", "Six strings and a body"),
        ("VIOLIN", "Played with a bow under the chin"),
        ("MELODY", "The tune you hum"),
        ("ORCHESTRA", "Large group of classical musicians"),
        ("SAXOPHONE", "Curved brass instrument of jazz"),
        ("HARMONICA", "Small mouth organ"),
        ("SYMPHONY", "Long work for a full orchestra"),
        ("PERCUSSION", "Family of instruments you strike"),
    ],
    "Science": [
        ("ATOM", "Smallest unit of an element"),
        ("CELL", "Basic unit of living things"),
        ("GRAVITY", "Force that pulls apples down"),
        ("MAGNET", "Attracts iron and has two poles"),
        ("MOLECULE", "Two or more atoms bonded"),
        ("ELECTRON", "Negatively charged particle"),
        ("EVOLUTION", "Change in species over generations"),
        ("THERMODYNAMICS", "Physics of heat and energy"),
        ("PHOTOSYNTHESIS", "Plants turning sunlight into sugar"),
        ("ELECTROMAGNETISM", "Force linking electricity and magnets"),
    ],
    "History": [
        ("ROME", "Empire built on seven hills"),
        ("PHARAOH", "Ruler of ancient Egypt"),
        ("SAMURAI", "Japanese warrior with a katana"),
        ("CRUSADES", "Medieval religious wars"),
        ("REVOLUTION", "Sudden overthrow of a government"),
        ("RENAISSANCE", "European rebirth of art and learning"),
        ("MESOPOTAMIA", "Land between two rivers"),
        ("INDUSTRIALREVOLUTION", "Age of factories and steam"),
        ("DECLARATIONOFINDEPENDENCE", "Signed in 1776"),
        ("BERLINWALL", "Barrier that fell in 1989"),
    ],
    "Geography": [
        ("DELTA", "Fan shaped river mouth"),
        ("ISLAND", "Land surrounded by water"),
        ("DESERT", "Very dry region with little rain"),
        ("PLATEAU", "Flat land raised high above"),
        ("PENINSULA", "Land with water on three sides"),
        ("EQUATOR", "Imaginary line around the middle"),
        ("ARCHIPELAGO", "A chain or group of islands"),
        ("LATITUDE", "Lines running east to west"),
        ("CONTINENT", "One of the seven big land masses"),
        ("TRIBUTARY", "Small river joining a bigger one"),
    ],
    "Colors": [
        ("RED", "Colour of blood and roses"),
        ("CYAN", "Between green and blue"),
        ("AMBER", "Warm orange yellow of traffic lights"),
        ("INDIGO", "Between blue and violet in a rainbow"),
        ("MAROON", "Dark brownish red"),
        ("MAGENTA", "Bright purplish pink"),
        ("TURQUOISE", "Blue green gemstone colour"),
        ("LAVENDER", "Pale purple like the flower"),
        ("CHARCOAL", "Very dark grey"),
        ("VERMILION", "Brilliant red orange pigment"),
    ],
    "Professions": [
        ("CHEF", "Runs the kitchen"),
        ("NURSE", "Cares for patients in a hospital"),
        ("PILOT", "Flies an aircraft"),
        ("TEACHER", "Works in a classroom"),
        ("ENGINEER", "Designs and builds things"),
        ("ARCHITECT", "Draws plans for buildings"),
        ("JOURNALIST", "Reports the news"),
        ("VETERINARIAN", "Doctor for animals"),
        ("PHOTOGRAPHER", "Captures images for a living"),
        ("ANAESTHETIST", "Doctor who puts you to sleep for surgery"),
    ],
    "Instruments": [
        ("FLUTE", "Blown sideways, made of metal or bamboo"),
        ("TABLA", "Pair of Indian hand drums"),
        ("BANJO", "Round bodied string instrument of folk music"),
        ("TRUMPET", "Brass instrument with three valves"),
        ("SITAR", "Long necked Indian string instrument"),
        ("CLARINET", "Black woodwind with a single reed"),
        ("ACCORDION", "Squeezebox with keys and bellows"),
        ("XYLOPHONE", "Wooden bars hit with mallets"),
        ("DIDGERIDOO", "Long droning Australian wind instrument"),
        ("HARPSICHORD", "Keyboard whose strings are plucked"),
    ],
    "Mythology": [
        ("ZEUS", "Greek king of the gods"),
        ("ODIN", "Norse all father with one eye"),
        ("MEDUSA", "Snakes for hair, turns you to stone"),
        ("PHOENIX", "Bird reborn from its own ashes"),
        ("MINOTAUR", "Bull headed beast in a labyrinth"),
        ("POSEIDON", "Greek god of the sea"),
        ("VALKYRIE", "Norse chooser of the slain"),
        ("PROMETHEUS", "Titan who stole fire for humans"),
        ("HANUMAN", "Devoted monkey god of great strength"),
        ("PERSEPHONE", "Queen of the underworld for half the year"),
    ],
    "Ocean": [
        ("CRAB", "Sideways walker with claws"),
        ("SHARK", "Feared fish with rows of teeth"),
        ("CORAL", "Colourful reef builder"),
        ("DOLPHIN", "Clever mammal that leaps and clicks"),
        ("OCTOPUS", "Eight arms and three hearts"),
        ("JELLYFISH", "Transparent stinger drifting along"),
        ("SEAHORSE", "Fish where the male carries the eggs"),
        ("SUBMARINE", "Vessel that travels underwater"),
        ("PLANKTON", "Tiny drifting food of the sea"),
        ("MARIANATRENCH", "Deepest point of the ocean"),
    ],
    "Weather": [
        ("FOG", "Cloud sitting on the ground"),
        ("HAIL", "Balls of ice falling from the sky"),
        ("STORM", "Wind, rain and thunder together"),
        ("CYCLONE", "Spinning tropical storm system"),
        ("DROUGHT", "Long period with no rain"),
        ("BLIZZARD", "Heavy snow with fierce wind"),
        ("HUMIDITY", "Amount of moisture in the air"),
        ("MONSOON", "Seasonal rain bearing wind"),
        ("THUNDERSTORM", "Lightning and loud rumbles"),
        ("PRECIPITATION", "Any water falling from clouds"),
    ],
    "Books": [
        ("ODYSSEY", "Homer's long journey home"),
        ("DRACULA", "Vampire novel set partly in Transylvania"),
        ("HAMLET", "To be or not to be"),
        ("MOBYDICK", "Captain hunts a great white whale"),
        ("WARANDPEACE", "Long Russian novel by Tolstoy"),
        ("THEHOBBIT", "Bilbo goes there and back again"),
        ("ANIMALFARM", "Farm animals overthrow the farmer"),
        ("FRANKENSTEIN", "Scientist creates a living creature"),
        ("PRIDEANDPREJUDICE", "Elizabeth meets Mr Darcy"),
        ("CRIMEANDPUNISHMENT", "Raskolnikov's guilt"),
    ],
}


# ----------------------------------------------------------------------
# 3. LEVEL SYSTEM: 10 main levels x 10 sub-levels = 100 sub-levels
# ----------------------------------------------------------------------

LEVEL_NAMES = [
    "Beginner",
    "Rookie",
    "Explorer",
    "Challenger",
    "Skilled",
    "Expert",
    "Master",
    "Champion",
    "Grandmaster",
    "Legend",
]


def difficulty_score(word, hint):
    """A simple numeric difficulty: longer words and more unique letters are harder."""
    return len(word) * 2 + len(set(word))


def build_levels():
    """
    Build LEVELS = { level_number : [ (theme, word, hint) x 10 ] }.

    Every word from every theme is scored, sorted from easy to hard and then
    split into 10 equal bands. Band 1 fills main level 1, band 10 fills main
    level 10, so difficulty always increases from Level 1 to Level 10.
    """
    pool = []
    for theme, entries in THEMES.items():
        for word, hint in entries:
            pool.append((theme, word, hint))

    # Sort easy -> hard, then a fixed shuffle inside so themes are mixed.
    pool.sort(key=lambda item: difficulty_score(item[1], item[2]))

    levels = {}
    band = len(pool) // 10  # words available per main level
    rng = random.Random(2026)  # fixed seed => same levels for everyone
    for level in range(1, 11):
        chunk = pool[(level - 1) * band: level * band]
        rng.shuffle(chunk)
        levels[level] = chunk[:10]  # exactly 10 sub-levels
    return levels


LEVELS = build_levels()


# ----------------------------------------------------------------------
# 4. ASCII HANGMAN  (7 stages: 0 to 6 wrong guesses)
# ----------------------------------------------------------------------

HANGMAN_STAGES = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
   =========""",
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
   =========""",
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
   =========""",
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
   =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
   =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
   =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
   ========="""
    ,
]

MAX_WRONG = 6  # exactly six wrong chances per word


# ----------------------------------------------------------------------
# 5. ACHIEVEMENTS
# ----------------------------------------------------------------------

ACHIEVEMENTS = {
    "FIRST_WIN": "First Blood - win your very first word",
    "PERFECT": "Flawless - win a word without a single mistake",
    "NO_HINT_5": "Self Made - win 5 words without using a hint",
    "WIN_10": "Word Hunter - win 10 words",
    "WIN_25": "Word Master - win 25 words",
    "STREAK_5": "On Fire - win 5 words in a row",
    "SURVIVOR": "Survivor - clear 5 words in one Survival run",
    "LEVEL_2": "Climbing - unlock main level 2",
    "LEVEL_5": "Halfway Hero - unlock main level 5",
    "LEGEND": "Legend - unlock main level 10",
    "SCORE_1000": "High Roller - reach 1000 total score",
    "CHALLENGER": "Challenge Accepted - finish a Challenge run",
}


# ----------------------------------------------------------------------
# 6. PLAYER CLASS  (all progress kept in memory, pure Python)
# ----------------------------------------------------------------------


class Player:
    """Holds one account: credentials, stats, progress and achievements."""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0
        self.best_score = 0
        self.wins = 0
        self.losses = 0
        self.streak = 0
        self.best_streak = 0
        self.hints_used = 0
        self.no_hint_wins = 0
        self.games_played = 0
        self.unlocked_level = 1        # highest main level unlocked
        self.unlocked_sub = 1          # highest sub-level unlocked in that level
        self.completed = set()         # set of (level, sub) already cleared
        self.badges = set()            # unlocked achievement keys

    # --- score helpers -------------------------------------------------
    def add_score(self, points):
        self.score += points
        if self.score < 0:
            self.score = 0
        if self.score > self.best_score:
            self.best_score = self.score

    # --- achievement helper --------------------------------------------
    def unlock(self, key):
        """Award a badge once and announce it."""
        if key in ACHIEVEMENTS and key not in self.badges:
            self.badges.add(key)
            print(paint(f"  ACHIEVEMENT UNLOCKED: {ACHIEVEMENTS[key]}", C.MAGENTA + C.BOLD))

    def check_achievements(self):
        if self.wins >= 1:
            self.unlock("FIRST_WIN")
        if self.wins >= 10:
            self.unlock("WIN_10")
        if self.wins >= 25:
            self.unlock("WIN_25")
        if self.best_streak >= 5:
            self.unlock("STREAK_5")
        if self.no_hint_wins >= 5:
            self.unlock("NO_HINT_5")
        if self.score >= 1000:
            self.unlock("SCORE_1000")
        if self.unlocked_level >= 2:
            self.unlock("LEVEL_2")
        if self.unlocked_level >= 5:
            self.unlock("LEVEL_5")
        if self.unlocked_level >= 10:
            self.unlock("LEGEND")

    # --- progress helpers ----------------------------------------------
    def is_unlocked(self, level, sub):
        """A sub-level is playable if it is already done or is the current edge."""
        if (level, sub) in self.completed:
            return True
        if level < self.unlocked_level:
            return True
        if level == self.unlocked_level and sub <= self.unlocked_sub:
            return True
        return False

    def complete_sublevel(self, level, sub):
        """Mark a sub-level as cleared and unlock what comes next."""
        first_time = (level, sub) not in self.completed
        self.completed.add((level, sub))

        if first_time:
            bonus = 25 * level
            self.add_score(bonus)
            print(paint(f"  Level completion bonus: +{bonus} points!", C.GREEN))

        # Unlock the next sub-level, or the next main level after all ten.
        if level == self.unlocked_level and sub == self.unlocked_sub:
            if sub < 10:
                self.unlocked_sub += 1
                print(paint(f"  Sub-level {level}-{sub + 1} unlocked!", C.CYAN))
            elif level < 10:
                self.unlocked_level += 1
                self.unlocked_sub = 1
                name = LEVEL_NAMES[self.unlocked_level - 1]
                print(paint(f"  MAIN LEVEL {self.unlocked_level} ({name}) UNLOCKED!", C.YELLOW + C.BOLD))
            else:
                print(paint("  You have completed ALL 100 sub-levels. LEGEND!", C.MAGENTA + C.BOLD))
        self.check_achievements()

    def level_progress(self, level):
        """How many sub-levels of a main level are finished."""
        return sum(1 for (lv, _s) in self.completed if lv == level)


# In-memory account store: username -> Player
ACCOUNTS = {}


# ----------------------------------------------------------------------
# 7. DISPLAY HELPERS
# ----------------------------------------------------------------------


def masked_word(word, guessed):
    """Show the word with underscores for letters not yet guessed."""
    out = []
    for ch in word:
        if ch.isalpha():
            out.append(ch if ch in guessed else "_")
        else:
            out.append(ch)
    return " ".join(out)


def letter_board(guessed, word):
    """Draw the A-Z board: green = correct, red = wrong, grey = untouched."""
    rows = []
    letters = list(string.ascii_uppercase)
    for start in range(0, 26, 13):
        cells = []
        for ch in letters[start:start + 13]:
            if ch in guessed and ch in word:
                cells.append(paint(ch, C.GREEN + C.BOLD))
            elif ch in guessed:
                cells.append(paint("x", C.RED))
            else:
                cells.append(paint(ch, C.GREY))
        rows.append("  " + " ".join(cells))
    return "\n".join(rows)


def hearts(left):
    """Chances left drawn as symbols."""
    return paint("* " * left, C.RED) + paint(". " * (MAX_WRONG - left), C.GREY)


def draw_screen(player, theme, word, guessed, wrong, label, hints_left):
    """Draw the whole game screen for one turn."""
    print("\n" * 1)
    title(f"HANGMAN  |  {label}")
    print(paint(HANGMAN_STAGES[wrong], C.WHITE))
    print()
    print("  Theme    : " + paint(theme, C.CYAN))
    print("  Player   : " + paint(player.username, C.CYAN) +
          "     Score: " + paint(str(player.score), C.YELLOW))
    print("  Chances  : " + hearts(MAX_WRONG - wrong) +
          paint(f" ({MAX_WRONG - wrong}/{MAX_WRONG})", C.GREY))
    print("  Hints    : " + paint(str(hints_left), C.MAGENTA) + " left")
    rule()
    print("   " + paint(masked_word(word, guessed), C.BOLD + C.WHITE))
    rule()
    print(letter_board(guessed, word))
    rule()


# ----------------------------------------------------------------------
# 8. CORE ROUND: play exactly one word
# ----------------------------------------------------------------------


def play_word(player, theme, word, hint, label, hints_allowed=1, level=1):
    """
    Play a single word.
    Returns True if the player guessed it, False if they ran out of chances.
    """
    word = word.upper()
    guessed = set()
    wrong = 0
    hints_left = hints_allowed
    hint_penalty = 0
    revealed_by_hint = 0
    unique_letters = {ch for ch in word if ch.isalpha()}

    while True:
        draw_screen(player, theme, word, guessed, wrong, label, hints_left)

        # ---- win check ----
        if unique_letters <= guessed:
            base = 10 * len(unique_letters)
            chance_bonus = (MAX_WRONG - wrong) * 15
            level_bonus = 10 * level
            perfect_bonus = 50 if wrong == 0 else 0
            gained = base + chance_bonus + level_bonus + perfect_bonus - hint_penalty
            if gained < 5:
                gained = 5

            player.wins += 1
            player.games_played += 1
            player.streak += 1
            player.best_streak = max(player.best_streak, player.streak)
            if revealed_by_hint == 0:
                player.no_hint_wins += 1
            player.add_score(gained)

            print(paint("\n   * * *  Y O U   W I N !  * * *", C.GREEN + C.BOLD))
            print("   The word was: " + paint(word, C.YELLOW + C.BOLD))
            print(f"   Base {base}  +  chances {chance_bonus}  +  level {level_bonus}"
                  f"  +  perfect {perfect_bonus}  -  hints {hint_penalty}")
            print(paint(f"   Points earned: +{gained}", C.GREEN))
            if wrong == 0:
                player.unlock("PERFECT")
            player.check_achievements()
            pause()
            return True

        # ---- lose check ----
        if wrong >= MAX_WRONG:
            player.losses += 1
            player.games_played += 1
            player.streak = 0
            player.add_score(-10)
            print(paint("\n   X X X   G A M E   O V E R   X X X", C.RED + C.BOLD))
            # The answer is revealed ONLY here, after all 6 chances are gone.
            print("   The correct word was: " + paint(word, C.YELLOW + C.BOLD))
            print("   Hint was: " + paint(hint, C.CYAN))
            print(paint("   -10 points. Better luck next time!", C.RED))
            pause()
            return False

        # ---- input ----
        print(paint("   Type a letter, or type 'hint' / 'quit'", C.GREY))
        choice = input(paint("   > ", C.BOLD)).strip().upper()

        # Only full words are commands, so single letters like Q and H stay guessable.
        if choice in ("QUIT", "EXIT"):
            print(paint("   Round abandoned.", C.YELLOW))
            player.streak = 0
            pause()
            return False

        if choice in ("HINT", "?"):
            if hints_left <= 0:
                print(paint("   No hints left for this word!", C.RED))
                pause()
                continue
            hints_left -= 1
            player.hints_used += 1
            revealed_by_hint += 1
            hint_penalty += 30
            print(paint(f"\n   HINT: {hint}", C.CYAN + C.BOLD))
            # A second hint on the same word also opens one free letter.
            if revealed_by_hint >= 2:
                remaining = sorted(unique_letters - guessed)
                if remaining:
                    free = random.choice(remaining)
                    guessed.add(free)
                    print(paint(f"   Bonus reveal: the letter {free}", C.CYAN))
            print(paint("   (-30 points from this word's reward)", C.GREY))
            pause()
            continue

        if len(choice) != 1 or choice not in string.ascii_uppercase:
            print(paint("   Please enter a single letter A-Z.", C.RED))
            pause()
            continue

        if choice in guessed:
            # Repeated guesses never cost a chance.
            print(paint(f"   You already tried '{choice}'. No chance lost.", C.YELLOW))
            pause()
            continue

        guessed.add(choice)
        if choice in unique_letters:
            count = word.count(choice)
            print(paint(f"   Correct! '{choice}' appears {count} time(s).", C.GREEN))
        else:
            wrong += 1
            print(paint(f"   Wrong! '{choice}' is not in the word. "
                        f"{MAX_WRONG - wrong} chance(s) left.", C.RED))
        pause(0)


def pause(kind=1):
    """Small pause so the player can read the message."""
    if kind:
        input(paint("   (press Enter to continue)", C.GREY))
    else:
        input(paint("   (Enter)", C.GREY))


# ----------------------------------------------------------------------
# 9. GAME MODES
# ----------------------------------------------------------------------


def hints_for_level(level):
    """Higher levels get fewer free hints."""
    if level <= 3:
        return 3
    if level <= 6:
        return 2
    return 1


def mode_classic(player):
    """Pick a main level, then a sub-level, and play that word."""
    level = choose_level(player)
    if level is None:
        return
    sub = choose_sublevel(player, level)
    if sub is None:
        return
    theme, word, hint = LEVELS[level][sub - 1]
    label = f"Classic  Level {level} ({LEVEL_NAMES[level - 1]})  Sub-level {sub}"
    won = play_word(player, theme, word, hint, label,
                    hints_allowed=hints_for_level(level), level=level)
    if won:
        player.complete_sublevel(level, sub)
        pause()


def mode_survival(player):
    """Keep playing random words until you lose one. Chances reset each word."""
    title("SURVIVAL MODE - one loss ends the run")
    print("  Words get harder as you survive. Good luck!\n")
    pause()
    cleared = 0
    while True:
        level = min(10, 1 + cleared)
        theme, word, hint = random.choice(LEVELS[level])
        label = f"Survival  streak {cleared}"
        won = play_word(player, theme, word, hint, label,
                        hints_allowed=1, level=level)
        if not won:
            break
        cleared += 1
        player.add_score(20 * cleared)  # survival bonus grows
        print(paint(f"   Survival bonus +{20 * cleared}!", C.GREEN))
        if cleared >= 5:
            player.unlock("SURVIVOR")
        pause()
    title(f"SURVIVAL OVER - you cleared {cleared} word(s)")
    player.check_achievements()
    pause()


def mode_random_theme(player):
    """A random theme picks a random word for you."""
    theme = random.choice(list(THEMES.keys()))
    word, hint = random.choice(THEMES[theme])
    title(f"RANDOM THEME:  {theme}")
    pause()
    play_word(player, theme, word, hint, f"Random Theme - {theme}",
              hints_allowed=2, level=3)


def mode_theme_pick(player):
    """Player chooses a theme, game chooses a random word from it."""
    theme = choose_theme()
    if theme is None:
        return
    word, hint = random.choice(THEMES[theme])
    play_word(player, theme, word, hint, f"Theme - {theme}",
              hints_allowed=2, level=3)


def mode_challenge(player):
    """5 hard words in a row, only ONE hint for the entire run."""
    title("CHALLENGE MODE - 5 hard words, 1 hint total")
    pause()
    hints_left = 1
    won_count = 0
    for round_no in range(1, 6):
        level = random.choice([7, 8, 9, 10])
        theme, word, hint = random.choice(LEVELS[level])
        label = f"Challenge  round {round_no}/5"
        won = play_word(player, theme, word, hint, label,
                        hints_allowed=hints_left, level=level)
        if won:
            won_count += 1
    total = won_count * 60
    player.add_score(total)
    title(f"CHALLENGE FINISHED - {won_count}/5 words  (+{total} points)")
    player.unlock("CHALLENGER")
    player.check_achievements()
    pause()


# ----------------------------------------------------------------------
# 10. SELECTION SCREENS
# ----------------------------------------------------------------------


def choose_theme():
    """List all themes in columns and let the player pick one."""
    names = sorted(THEMES.keys())
    title(f"THEMES  ({len(names)} available)")
    for i in range(0, len(names), 3):
        row = ""
        for j, name in enumerate(names[i:i + 3]):
            row += f"{paint(str(i + j + 1).rjust(2), C.YELLOW)}. {name:<18}"
        print("  " + row)
    rule()
    raw = input(paint("  Theme number (or 0 to go back): ", C.BOLD)).strip()
    if not raw.isdigit():
        return None
    num = int(raw)
    if num < 1 or num > len(names):
        return None
    return names[num - 1]


def choose_level(player):
    """Show the 10 main levels with lock status and progress."""
    title("MAIN LEVELS")
    for lv in range(1, 11):
        name = LEVEL_NAMES[lv - 1]
        done = player.level_progress(lv)
        if lv <= player.unlocked_level:
            bar = "#" * done + "." * (10 - done)
            print(f"  {paint(str(lv).rjust(2), C.YELLOW)}. "
                  f"{paint(name.ljust(13), C.GREEN)} [{bar}] {done}/10 sub-levels")
        else:
            print(f"  {paint(str(lv).rjust(2), C.GREY)}. "
                  f"{paint(name.ljust(13), C.GREY)} {paint('[LOCKED]', C.RED)}")
    rule()
    raw = input(paint("  Level number (0 to go back): ", C.BOLD)).strip()
    if not raw.isdigit():
        return None
    lv = int(raw)
    if lv < 1 or lv > 10:
        return None
    if lv > player.unlocked_level:
        print(paint("  That level is locked. Finish the earlier levels first!", C.RED))
        pause()
        return None
    return lv


def choose_sublevel(player, level):
    """Show the 10 sub-levels of a main level with lock/clear status."""
    title(f"LEVEL {level} - {LEVEL_NAMES[level - 1]}  (sub-levels)")
    for sub in range(1, 11):
        theme, word, _hint = LEVELS[level][sub - 1]
        length = f"{len(word)} letters"
        if (level, sub) in player.completed:
            state = paint("[CLEARED]", C.GREEN)
        elif player.is_unlocked(level, sub):
            state = paint("[OPEN]   ", C.YELLOW)
        else:
            state = paint("[LOCKED] ", C.RED)
        print(f"  {str(sub).rjust(2)}. {state}  theme: {theme:<16} {length}")
    rule()
    raw = input(paint("  Sub-level number (0 to go back): ", C.BOLD)).strip()
    if not raw.isdigit():
        return None
    sub = int(raw)
    if sub < 1 or sub > 10:
        return None
    if not player.is_unlocked(level, sub):
        print(paint("  Locked! Complete the previous sub-level first.", C.RED))
        pause()
        return None
    return sub


# ----------------------------------------------------------------------
# 11. INFO SCREENS
# ----------------------------------------------------------------------


def show_statistics(player):
    title(f"STATISTICS - {player.username}")
    played = player.games_played
    rate = (player.wins / played * 100) if played else 0.0
    lines = [
        ("Total score", player.score),
        ("Best score", player.best_score),
        ("Words played", played),
        ("Wins", player.wins),
        ("Losses", player.losses),
        ("Win rate", f"{rate:.1f}%"),
        ("Current streak", player.streak),
        ("Best streak", player.best_streak),
        ("Hints used", player.hints_used),
        ("Wins without hints", player.no_hint_wins),
        ("Main level unlocked", f"{player.unlocked_level} ({LEVEL_NAMES[player.unlocked_level - 1]})"),
        ("Sub-levels cleared", f"{len(player.completed)}/100"),
    ]
    for name, value in lines:
        print(f"  {name:<22}: " + paint(str(value), C.YELLOW))
    rule()
    print(paint(f"  ACHIEVEMENTS ({len(player.badges)}/{len(ACHIEVEMENTS)})", C.BOLD))
    for key, text in ACHIEVEMENTS.items():
        if key in player.badges:
            print("   " + paint("[x] " + text, C.GREEN))
        else:
            print("   " + paint("[ ] " + text, C.GREY))
    rule()
    pause()


def show_themes():
    names = sorted(THEMES.keys())
    total = sum(len(v) for v in THEMES.values())
    title(f"THEME LIST - {len(names)} themes, {total} words")
    for i in range(0, len(names), 3):
        row = ""
        for j, name in enumerate(names[i:i + 3]):
            row += f"{paint(str(i + j + 1).rjust(2), C.YELLOW)}. {name:<18}"
        print("  " + row)
    rule()
    pause()


def show_levels(player):
    title("LEVEL OVERVIEW")
    for lv in range(1, 11):
        done = player.level_progress(lv)
        status = paint("OPEN", C.GREEN) if lv <= player.unlocked_level else paint("LOCKED", C.RED)
        bar = "#" * done + "." * (10 - done)
        print(f"  Level {str(lv).rjust(2)}  {LEVEL_NAMES[lv - 1]:<13} [{bar}] {done}/10   {status}")
    rule()
    print(paint("  Clear all 10 sub-levels of a level to unlock the next one.", C.GREY))
    pause()


def how_to_play():
    title("HOW TO PLAY")
    text = [
        "1. A hidden word is shown as underscores, one per letter.",
        "2. Type one letter A-Z and press Enter to guess it.",
        "3. A correct letter is revealed everywhere it appears.",
        "4. A wrong letter costs ONE of your 6 chances and draws",
        "   the next part of the hangman.",
        "5. Guessing the SAME letter again costs nothing.",
        "6. Type 'hint' for a clue. Hints are limited and reduce",
        "   the points you earn for that word (-30 each).",
        "7. Type 'quit' to leave the round early.",
        "8. The answer is only revealed after all 6 chances are lost.",
        "",
        "SCORING",
        "  +10 per unique letter in the word",
        "  +15 per unused chance",
        "  +10 x level number",
        "  +50 perfect bonus (zero mistakes)",
        "  +25 x level as a sub-level completion bonus",
        "  -30 per hint,  -10 for a loss",
        "",
        "MODES",
        "  Classic      - choose a level and sub-level",
        "  Theme        - choose one of 36 themes",
        "  Survival     - endless words, one loss ends the run",
        "  Random Theme - the game surprises you",
        "  Challenge    - 5 hard words, only 1 hint in total",
        "",
        "PROGRESS",
        "  Win a sub-level to unlock the next one.",
        "  Clear all 10 sub-levels to unlock the next main level.",
        "  Locked levels cannot be played.",
    ]
    for line in text:
        print("  " + line)
    rule()
    pause()


# ----------------------------------------------------------------------
# 12. LOGIN / SIGNUP
# ----------------------------------------------------------------------


def signup():
    """Create a new account in memory."""
    title("SIGN UP")
    username = input("  Choose a username: ").strip()
    if not username:
        print(paint("  Username cannot be empty.", C.RED))
        pause()
        return None
    if username in ACCOUNTS:
        print(paint("  That username is already taken.", C.RED))
        pause()
        return None
    password = input("  Choose a password (min 4 chars): ").strip()
    if len(password) < 4:
        print(paint("  Password too short.", C.RED))
        pause()
        return None
    confirm = input("  Confirm password: ").strip()
    if password != confirm:
        print(paint("  Passwords do not match.", C.RED))
        pause()
        return None
    ACCOUNTS[username] = Player(username, password)
    print(paint(f"  Account created. Welcome, {username}!", C.GREEN))
    pause()
    return ACCOUNTS[username]


def login():
    """Log into an existing in-memory account."""
    title("LOGIN")
    if not ACCOUNTS:
        print(paint("  No accounts yet - please sign up first.", C.YELLOW))
        pause()
        return None
    username = input("  Username: ").strip()
    password = input("  Password: ").strip()
    player = ACCOUNTS.get(username)
    if player is None or player.password != password:
        print(paint("  Wrong username or password.", C.RED))
        pause()
        return None
    print(paint(f"  Welcome back, {username}!", C.GREEN))
    pause()
    return player


DEMO_USER = "demo"
DEMO_PASS = "demo123"


def make_demo_player():
    """Build a fresh demo account with the preset starting progress."""
    player = Player(DEMO_USER, DEMO_PASS)
    player.score = 500
    player.best_score = 500
    player.wins = 5
    player.games_played = 5
    player.unlocked_level = 3
    player.unlocked_sub = 10
    for lvl in (1, 2):
        for sub in range(1, 11):
            player.completed.add((lvl, sub))
    ACCOUNTS[DEMO_USER] = player
    return player


def demo_login():
    """Instantly log into a preset demo account for quick testing."""
    title("DEMO LOGIN")
    player = ACCOUNTS.get(DEMO_USER)
    if player is None:
        player = make_demo_player()
    print(paint(f"  Logged in as '{DEMO_USER}' (password: {DEMO_PASS}).", C.GREEN))
    print("  Levels 1-3 are already unlocked. Have fun testing!")
    pause()
    return player


def reset_demo():
    """Wipe only the demo account and rebuild it at levels 1-3."""
    title("RESET DEMO")
    if DEMO_USER not in ACCOUNTS:
        print(paint("  No demo progress to reset - it will start fresh anyway.", C.YELLOW))
        pause()
        return
    confirm = input("  Erase all demo progress? (y/n): ").strip().lower()
    if confirm != "y":
        print(paint("  Reset cancelled.", C.YELLOW))
        pause()
        return
    ACCOUNTS.pop(DEMO_USER, None)
    make_demo_player()
    print(paint("  Demo account reset. Score 500, levels 1-3 unlocked.", C.GREEN))
    print("  Other accounts were not touched.")
    pause()


def auth_menu():
    """Start screen: login, signup, demo or exit. Returns a Player or None."""
    while True:
        title("A D V A N C E D   H A N G M A N")
        print(paint("        Pure Python  |  36 themes  |  100 sub-levels\n", C.CYAN))
        print("   1. Login")
        print("   2. Sign up")
        print("   3. Demo login (play instantly)")
        print("   4. Reset demo (clear demo progress)")
        print("   5. Exit")
        rule()
        choice = input(paint("   Choose: ", C.BOLD)).strip()
        if choice == "1":
            player = login()
            if player:
                return player
        elif choice == "2":
            player = signup()
            if player:
                return player
        elif choice == "3":
            return demo_login()
        elif choice == "4":
            reset_demo()
        elif choice == "5":
            return None
        else:
            print(paint("   Invalid choice.", C.RED))
            pause()



# ----------------------------------------------------------------------
# 13. MENUS
# ----------------------------------------------------------------------


def play_menu(player):
    """Sub-menu with all the game modes."""
    while True:
        title("PLAY")
        print("   1. Classic      (levels and sub-levels)")
        print("   2. Theme        (choose one of 36 themes)")
        print("   3. Survival     (until you lose)")
        print("   4. Random Theme (surprise me)")
        print("   5. Challenge    (5 hard words, 1 hint)")
        print("   6. Back to main menu")
        rule()
        choice = input(paint("   Choose: ", C.BOLD)).strip()
        if choice == "1":
            mode_classic(player)
        elif choice == "2":
            mode_theme_pick(player)
        elif choice == "3":
            mode_survival(player)
        elif choice == "4":
            mode_random_theme(player)
        elif choice == "5":
            mode_challenge(player)
        elif choice == "6":
            return
        else:
            print(paint("   Invalid choice.", C.RED))
            pause()


def main_menu(player):
    """Main menu. Returns True to log out, False to quit the program."""
    while True:
        title(f"MAIN MENU  -  {player.username}")
        print("   Score: " + paint(str(player.score), C.YELLOW) +
              "   Best: " + paint(str(player.best_score), C.YELLOW) +
              "   Level: " + paint(str(player.unlocked_level), C.CYAN) +
              "   Cleared: " + paint(f"{len(player.completed)}/100", C.CYAN))
        rule()
        print("   1. Play")
        print("   2. Themes")
        print("   3. Levels")
        print("   4. Statistics")
        print("   5. How to Play")
        print("   6. Logout")
        print("   7. Exit game")
        rule()
        choice = input(paint("   Choose: ", C.BOLD)).strip()
        if choice == "1":
            play_menu(player)
        elif choice == "2":
            show_themes()
        elif choice == "3":
            show_levels(player)
        elif choice == "4":
            show_statistics(player)
        elif choice == "5":
            how_to_play()
        elif choice == "6":
            print(paint("   Logged out. Your progress stays for this session.", C.YELLOW))
            pause()
            return True
        elif choice == "7":
            return False
        else:
            print(paint("   Invalid choice.", C.RED))
            pause()


# ----------------------------------------------------------------------
# 14. ENTRY POINT
# ----------------------------------------------------------------------


def main():
    """Run the whole game loop: auth -> main menu -> logout/exit."""
    try:
        while True:
            player = auth_menu()
            if player is None:
                break
            keep_going = main_menu(player)
            if not keep_going:
                break
        title("THANKS FOR PLAYING ADVANCED HANGMAN!")
    except (KeyboardInterrupt, EOFError):
        print(paint("\n  Game closed. Bye!", C.YELLOW))


if __name__ == "__main__":
    main()
