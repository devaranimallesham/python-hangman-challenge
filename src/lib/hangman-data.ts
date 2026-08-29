export interface ThemeWord {
  word: string;
  hint: string;
}

export interface Theme {
  name: string;
  icon: string;
  words: ThemeWord[];
}

export const THEMES: Theme[] = [
  {
    name: "Video Games",
    icon: "🎮",
    words: [
      { word: "MINECRAFT", hint: "Blocky sandbox world" },
      { word: "ZELDA", hint: "Princess of Hyrule" },
      { word: "PACMAN", hint: "Yellow arcade icon" },
      { word: "FORTNITE", hint: "Battle royale building game" },
      { word: "TETRIS", hint: "Falling blocks puzzle" },
      { word: "MARIO", hint: "Italian plumber hero" },
      { word: "PORTAL", hint: "Cake is a lie" },
      { word: "HALO", hint: "Master Chief's series" },
      { word: "SONIC", hint: "Fast blue hedgehog" },
      { word: "DOOM", hint: "Demon-slaying shooter" },
    ],
  },
  {
    name: "Movies",
    icon: "🎬",
    words: [
      { word: "TITANIC", hint: "Unsinkable ship romance" },
      { word: "INCEPTION", hint: "Dreams within dreams" },
      { word: "AVATAR", hint: "Blue aliens of Pandora" },
      { word: "GLADIATOR", hint: "Roman arena revenge" },
      { word: "JAWS", hint: "Killer shark thriller" },
      { word: "FROZEN", hint: "Let it go" },
      { word: "ROCKY", hint: "Underdog boxer" },
      { word: "ALIEN", hint: "In space no one can hear you scream" },
      { word: "MATRIX", hint: "Red pill or blue pill" },
      { word: "CASABLANCA", hint: "We'll always have Paris" },
    ],
  },
  {
    name: "Animals",
    icon: "🦁",
    words: [
      { word: "ELEPHANT", hint: "Largest land mammal" },
      { word: "PENGUIN", hint: "Flightless Antarctic bird" },
      { word: "GIRAFFE", hint: "Longest neck" },
      { word: "OCTOPUS", hint: "Eight arms" },
      { word: "CHEETAH", hint: "Fastest land animal" },
      { word: "DOLPHIN", hint: "Intelligent sea mammal" },
      { word: "KANGAROO", hint: "Australian jumper" },
      { word: "GORILLA", hint: "Great ape" },
      { word: "FLAMINGO", hint: "Pink one-legged bird" },
      { word: "CHAMELEON", hint: "Color-changing lizard" },
    ],
  },
  {
    name: "Countries",
    icon: "🌍",
    words: [
      { word: "BRAZIL", hint: "Amazon rainforest nation" },
      { word: "JAPAN", hint: "Land of the rising sun" },
      { word: "EGYPT", hint: "Pyramids and the Nile" },
      { word: "CANADA", hint: "Maple leaf flag" },
      { word: "AUSTRALIA", hint: "The land down under" },
      { word: "FRANCE", hint: "Eiffel Tower country" },
      { word: "KENYA", hint: "Safari homeland" },
      { word: "ICELAND", hint: "Geysers and volcanoes" },
      { word: "MEXICO", hint: "Aztec heritage" },
      { word: "NORWAY", hint: "Fjords and Vikings" },
    ],
  },
  {
    name: "Food",
    icon: "🍕",
    words: [
      { word: "LASAGNA", hint: "Layered Italian pasta" },
      { word: "SUSHI", hint: "Japanese raw fish dish" },
      { word: "CROISSANT", hint: "Buttery French pastry" },
      { word: "BURRITO", hint: "Wrapped Mexican meal" },
      { word: "PANCAKES", hint: "Breakfast stack" },
      { word: "HUMMUS", hint: "Chickpea dip" },
      { word: "GUACAMOLE", hint: "Avocado dip" },
      { word: "WAFFLES", hint: "Grid-patterned breakfast" },
      { word: "DUMPLINGS", hint: "Steamed filled pockets" },
      { word: "CHOCOLATE", hint: "Cocoa-based treat" },
    ],
  },
  {
    name: "Space",
    icon: "🚀",
    words: [
      { word: "NEBULA", hint: "Cosmic gas cloud" },
      { word: "SATURN", hint: "Ringed planet" },
      { word: "COMET", hint: "Icy tailed wanderer" },
      { word: "ASTEROID", hint: "Rocky space object" },
      { word: "GALAXY", hint: "Collection of billions of stars" },
      { word: "TELESCOPE", hint: "Instrument for stargazing" },
      { word: "GRAVITY", hint: "Pull of massive objects" },
      { word: "ECLIPSE", hint: "Celestial shadow event" },
      { word: "METEOR", hint: "Shooting star" },
      { word: "ASTRONAUT", hint: "Space traveler" },
    ],
  },
  {
    name: "Sports",
    icon: "⚽",
    words: [
      { word: "BASKETBALL", hint: "Hoops game" },
      { word: "CRICKET", hint: "Bat and wicket game" },
      { word: "MARATHON", hint: "26.2 mile race" },
      { word: "GYMNASTICS", hint: "Flips and balance beam" },
      { word: "SKIING", hint: "Snow slope sport" },
      { word: "BOXING", hint: "Ring fighting" },
      { word: "SURFING", hint: "Riding ocean waves" },
      { word: "ARCHERY", hint: "Bow and arrow" },
      { word: "FENCING", hint: "Sword duel sport" },
      { word: "RUGBY", hint: "Oval ball contact sport" },
    ],
  },
  {
    name: "Music",
    icon: "🎵",
    words: [
      { word: "SYMPHONY", hint: "Large orchestral work" },
      { word: "UKULELE", hint: "Small Hawaiian guitar" },
      { word: "TROMBONE", hint: "Sliding brass instrument" },
      { word: "RHYTHM", hint: "Musical beat pattern" },
      { word: "CONCERT", hint: "Live music event" },
      { word: "HARMONY", hint: "Pleasing note combination" },
      { word: "VIOLIN", hint: "Four-string bowed instrument" },
      { word: "MELODY", hint: "Tune you hum" },
      { word: "ENCORE", hint: "Crowd demands more" },
      { word: "BASSOON", hint: "Low woodwind instrument" },
    ],
  },
  {
    name: "Science",
    icon: "🔬",
    words: [
      { word: "MOLECULE", hint: "Bonded atoms" },
      { word: "GRAVITY", hint: "Newton's apple force" },
      { word: "EVOLUTION", hint: "Darwin's theory" },
      { word: "BACTERIA", hint: "Microscopic organisms" },
      { word: "QUANTUM", hint: "Physics of the very small" },
      { word: "GENOME", hint: "Full DNA set" },
      { word: "ELECTRON", hint: "Negatively charged particle" },
      { word: "CHEMISTRY", hint: "Study of reactions" },
      { word: "FOSSIL", hint: "Ancient remains in rock" },
      { word: "MAGNETISM", hint: "Force of poles" },
    ],
  },
  {
    name: "Fantasy",
    icon: "🐉",
    words: [
      { word: "DRAGON", hint: "Fire-breathing beast" },
      { word: "WIZARD", hint: "Robe-wearing spellcaster" },
      { word: "UNICORN", hint: "Horned magical horse" },
      { word: "POTION", hint: "Brewed magical drink" },
      { word: "ENCHANTED", hint: "Under a spell" },
      { word: "GOBLIN", hint: "Mischievous cave creature" },
      { word: "CRYSTAL", hint: "Magical glowing stone" },
      { word: "KINGDOM", hint: "Realm ruled by royalty" },
      { word: "PHOENIX", hint: "Bird reborn from ashes" },
      { word: "SPELLBOOK", hint: "Tome of incantations" },
    ],
  },
  {
    name: "Professions",
    icon: "💼",
    words: [
      { word: "ARCHITECT", hint: "Designs buildings" },
      { word: "SURGEON", hint: "Operating room doctor" },
      { word: "PILOT", hint: "Flies aircraft" },
      { word: "CHEF", hint: "Professional cook" },
      { word: "JOURNALIST", hint: "Reports the news" },
      { word: "LAWYER", hint: "Argues in court" },
      { word: "ENGINEER", hint: "Builds and designs systems" },
      { word: "ASTRONOMER", hint: "Studies celestial objects" },
      { word: "FIREFIGHTER", hint: "Battles blazes" },
      { word: "PHARMACIST", hint: "Dispenses medicine" },
    ],
  },
  {
    name: "Nature",
    icon: "🌲",
    words: [
      { word: "WATERFALL", hint: "Cascading river drop" },
      { word: "VOLCANO", hint: "Erupting mountain" },
      { word: "RAINBOW", hint: "Arc after the rain" },
      { word: "GLACIER", hint: "Slow-moving river of ice" },
      { word: "MEADOW", hint: "Grassy open field" },
      { word: "THUNDER", hint: "Sound after lightning" },
      { word: "DESERT", hint: "Arid sandy region" },
      { word: "CANYON", hint: "Deep rocky gorge" },
      { word: "AURORA", hint: "Northern lights" },
      { word: "MANGROVE", hint: "Coastal swamp forest" },
    ],
  },
];

export interface Level {
  number: number;
  name: string;
  maxLength: number;
  scoreBonus: number;
}

export const LEVELS: Level[] = [
  { number: 1, name: "Rookie", maxLength: 5, scoreBonus: 1 },
  { number: 2, name: "Explorer", maxLength: 6, scoreBonus: 2 },
  { number: 3, name: "Apprentice", maxLength: 6, scoreBonus: 3 },
  { number: 4, name: "Challenger", maxLength: 7, scoreBonus: 4 },
  { number: 5, name: "Hunter", maxLength: 7, scoreBonus: 5 },
  { number: 6, name: "Warrior", maxLength: 8, scoreBonus: 6 },
  { number: 7, name: "Master", maxLength: 8, scoreBonus: 7 },
  { number: 8, name: "Champion", maxLength: 9, scoreBonus: 8 },
  { number: 9, name: "Legend", maxLength: 10, scoreBonus: 9 },
  { number: 10, name: "Immortal", maxLength: 99, scoreBonus: 10 },
];

export const MAX_WRONG = 6;
export const HINT_COST = 15;
export const BASE_WIN_SCORE = 50;

export const ACHIEVEMENTS = [
  { id: "first_win", name: "First Blood", desc: "Win your first word", icon: "🏆" },
  { id: "flawless", name: "Flawless", desc: "Win with zero wrong guesses", icon: "✨" },
  { id: "hat_trick", name: "Hat Trick", desc: "Win 3 words in a row", icon: "🎩" },
  { id: "survivor", name: "Survivor", desc: "Win 5 survival rounds", icon: "🛡️" },
  { id: "bookworm", name: "Bookworm", desc: "Play 5 different themes", icon: "📚" },
  { id: "halfway", name: "Halfway There", desc: "Unlock level 5", icon: "⛰️" },
  { id: "high_roller", name: "High Roller", desc: "Reach 1,000 total points", icon: "💰" },
  { id: "legend", name: "Legend", desc: "Reach the final level", icon: "👑" },
];
