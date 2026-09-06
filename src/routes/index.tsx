import { createFileRoute } from "@tanstack/react-router";
import {
  BarChart3,
  BookOpen,
  Check,
  ChevronRight,
  CircleHelp,
  Flame,
  Gamepad2,
  Gift,
  Grid2X2,
  Lightbulb,
  Lock,
  RotateCcw,
  Shield,
  Sparkles,
  Trophy,
  X,
  Zap,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { ACHIEVEMENTS, BASE_WIN_SCORE, HINT_COST, LEVELS, MAX_WRONG, THEMES } from "@/lib/hangman-data";

const STORAGE_KEY = "hangman-guest-progress";
const NAME_STORAGE_KEY = "hangman-player-name";
const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
const FALLBACK_THEME = { name: "Video Games", icon: "🎮", words: [{ word: "MINECRAFT", hint: "Blocky sandbox world" }] };
const FALLBACK_LEVEL = { number: 1, name: "Rookie", maxLength: 5, scoreBonus: 1 };
const FALLBACK_WORD = { word: "MINECRAFT", hint: "Blocky sandbox world" };
const NAV_ITEMS = [
  { id: "play", label: "Play", icon: Gamepad2 },
  { id: "themes", label: "Themes", icon: Grid2X2 },
  { id: "levels", label: "Levels", icon: Trophy },
  { id: "statistics", label: "Statistics", icon: BarChart3 },
  { id: "how-to-play", label: "How to play", icon: CircleHelp },
] as const;

type View = (typeof NAV_ITEMS)[number]["id"];
type Mode = "Classic" | "Survival" | "Random" | "Challenge";
type GameStatus = "playing" | "won" | "lost";

interface Progress {
  score: number;
  bestScore: number;
  wins: number;
  losses: number;
  streak: number;
  bestStreak: number;
  rounds: number;
  unlockedLevel: number;
  achievements: string[];
}

const DEFAULT_PROGRESS: Progress = {
  score: 0,
  bestScore: 0,
  wins: 0,
  losses: 0,
  streak: 0,
  bestStreak: 0,
  rounds: 0,
  unlockedLevel: 1,
  achievements: [],
};

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Hangman — Word Guessing Game" },
      { name: "description", content: "Play a fast, friendly Hangman word guessing game with themes, levels, hints, and achievements." },
      { property: "og:title", content: "Hangman — Word Guessing Game" },
      { property: "og:description", content: "Guess the word, protect the stick figure, and unlock every level." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

function Index() {
  const [view, setView] = useState<View>("play");
  const [hydrated, setHydrated] = useState(false);
  const [playerName, setPlayerName] = useState("");
  const [nameInput, setNameInput] = useState("");
  const [progress, setProgress] = useState<Progress>(DEFAULT_PROGRESS);
  const [mode, setMode] = useState<Mode>("Classic");
  const [themeIndex, setThemeIndex] = useState(0);
  const [levelNumber, setLevelNumber] = useState(1);
  const [word, setWord] = useState((THEMES[0] ?? FALLBACK_THEME).words[0]?.word ?? FALLBACK_WORD.word);
  const [activeThemeName, setActiveThemeName] = useState((THEMES[0] ?? FALLBACK_THEME).name);
  const [guessed, setGuessed] = useState<Set<string>>(new Set());
  const [wrongGuesses, setWrongGuesses] = useState(0);
  const [hintUsed, setHintUsed] = useState(false);
  const [status, setStatus] = useState<GameStatus>("playing");

  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      if (saved) setProgress({ ...DEFAULT_PROGRESS, ...JSON.parse(saved) });
      const savedName = window.localStorage.getItem(NAME_STORAGE_KEY);
      if (savedName) {
        setPlayerName(savedName);
        setNameInput(savedName);
      }
    } catch {
      // A private browsing session can deny storage; the game still works in memory.
    }
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (hydrated) window.localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }, [hydrated, progress]);

  const currentTheme = THEMES[themeIndex] ?? THEMES[0] ?? FALLBACK_THEME;
  const currentLevel = LEVELS[levelNumber - 1] ?? LEVELS[0] ?? FALLBACK_LEVEL;
  const maxChances = mode === "Challenge" ? 4 : MAX_WRONG;
  const revealedWord = useMemo(
    () => word.split("").map((letter) => (guessed.has(letter) ? letter : "_")),
    [guessed, word],
  );
  const isComplete = revealedWord.every((letter) => letter !== "_");
  const accuracy = progress.rounds === 0 ? 0 : Math.round((progress.wins / progress.rounds) * 100);

  const enterGame = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmedName = nameInput.trim();
    if (!trimmedName) return;
    setPlayerName(trimmedName);
    try {
      window.localStorage.setItem(NAME_STORAGE_KEY, trimmedName);
    } catch {
      // The game still works if storage is unavailable.
    }
  };

  const chooseWord = useCallback((nextMode = mode, nextThemeIndex = themeIndex, nextLevel = levelNumber) => {
    const theme = THEMES[nextThemeIndex] ?? THEMES[0] ?? FALLBACK_THEME;
    const level = LEVELS[nextLevel - 1] ?? LEVELS[0] ?? FALLBACK_LEVEL;
    const pool = nextMode === "Random" ? THEMES.flatMap((item) => item.words) : theme.words;
    const suitable = pool.filter((item) => item.word.length <= level.maxLength);
    const choices = suitable.length > 0 ? suitable : pool;
    const selected = choices[Math.floor(Math.random() * choices.length)] ?? theme.words[0] ?? FALLBACK_WORD;
    const sourceTheme = THEMES.find((item) => item.words.some((itemWord) => itemWord.word === selected.word));
    setWord(selected.word);
    setActiveThemeName(nextMode === "Random" ? sourceTheme?.name ?? "Random" : theme.name);
    setGuessed(new Set());
    setWrongGuesses(0);
    setHintUsed(false);
    setStatus("playing");
  }, [levelNumber, mode, themeIndex]);

  const startRound = (nextMode = mode, nextThemeIndex = themeIndex, nextLevel = levelNumber) => {
    setMode(nextMode);
    setThemeIndex(nextThemeIndex);
    setLevelNumber(nextLevel);
    chooseWord(nextMode, nextThemeIndex, nextLevel);
    setView("play");
  };

  const finishRound = (won: boolean) => {
    setStatus(won ? "won" : "lost");
    setProgress((previous) => {
      const roundScore = won
        ? BASE_WIN_SCORE + currentLevel.scoreBonus * 10 + Math.max(0, (maxChances - wrongGuesses) * 5)
        : 0;
      const nextScore = Math.max(0, previous.score + roundScore);
      const nextWins = previous.wins + (won ? 1 : 0);
      const nextLosses = previous.losses + (won ? 0 : 1);
      const nextStreak = won ? previous.streak + 1 : 0;
      const earned = new Set(previous.achievements);
      if (won && nextWins >= 1) earned.add("first_win");
      if (won && wrongGuesses === 0 && !hintUsed) earned.add("flawless");
      if (won && nextStreak >= 3) earned.add("hat_trick");
      if (won && nextWins >= 5) earned.add("survivor");
      if (won && nextScore >= 1000) earned.add("high_roller");
      return {
        ...previous,
        score: nextScore,
        bestScore: Math.max(previous.bestScore, roundScore),
        wins: nextWins,
        losses: nextLosses,
        rounds: previous.rounds + 1,
        streak: nextStreak,
        bestStreak: Math.max(previous.bestStreak, nextStreak),
        unlockedLevel: won ? Math.min(10, Math.max(previous.unlockedLevel, levelNumber + 1)) : previous.unlockedLevel,
        achievements: [...earned],
      };
    });
  };

  const handleGuess = (letter: string) => {
    if (status !== "playing" || guessed.has(letter)) return;
    const nextGuessed = new Set(guessed);
    nextGuessed.add(letter);
    setGuessed(nextGuessed);
    if (!word.includes(letter)) {
      const nextWrong = wrongGuesses + 1;
      setWrongGuesses(nextWrong);
      if (nextWrong >= maxChances) finishRound(false);
      return;
    }
    if (word.split("").every((character) => nextGuessed.has(character))) finishRound(true);
  };

  const useHint = () => {
    if (status !== "playing" || hintUsed || progress.score < HINT_COST) return;
    const missingLetter = word.split("").find((letter) => !guessed.has(letter));
    if (!missingLetter) return;
    const nextGuessed = new Set(guessed);
    nextGuessed.add(missingLetter);
    setGuessed(nextGuessed);
    setHintUsed(true);
    setProgress((previous) => ({ ...previous, score: Math.max(0, previous.score - HINT_COST) }));
    if (word.split("").every((character) => nextGuessed.has(character))) finishRound(true);
  };

  const renderView = () => {
    if (view === "themes") {
      return <ThemesView selectedTheme={themeIndex} onSelect={(index) => startRound(mode, index, levelNumber)} />;
    }
    if (view === "levels") {
      return <LevelsView unlockedLevel={progress.unlockedLevel} selectedLevel={levelNumber} onSelect={(level) => startRound(mode, themeIndex, level)} />;
    }
    if (view === "statistics") return <StatisticsView progress={progress} accuracy={accuracy} />;
    if (view === "how-to-play") return <HowToPlayView />;
    return (
      <PlayView
        mode={mode}
        themeName={activeThemeName}
        level={currentLevel}
        word={word}
        revealedWord={revealedWord}
        guessed={guessed}
        wrongGuesses={wrongGuesses}
        maxChances={maxChances}
        hintUsed={hintUsed}
        status={status}
        score={progress.score}
         playerName={playerName}
        onModeChange={(nextMode) => startRound(nextMode)}
        onGuess={handleGuess}
        onHint={useHint}
        onRestart={() => chooseWord()}
      />
    );
  };

  if (!hydrated) {
    return <div className="min-h-screen bg-paper" aria-label="Loading Hangman" />;
  }

  if (!playerName) {
    return <NameEntry name={nameInput} onNameChange={setNameInput} onSubmit={enterGame} />;
  }

  return (
    <div className="min-h-screen bg-paper text-ink">
      <header className="border-b border-line bg-paper/95 backdrop-blur-sm">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between px-5 py-4 lg:px-10">
          <button className="flex items-center gap-3 text-left" onClick={() => setView("play")} aria-label="Go to Hangman play screen">
            <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-ink text-paper shadow-sm"><Gamepad2 size={20} /></span>
            <span><span className="block font-display text-lg font-bold tracking-[0.08em]">HANGMAN</span><span className="block text-[10px] font-bold uppercase tracking-[0.2em] text-ink/50">Word guessing club</span></span>
          </button>
          <div className="hidden items-center gap-3 sm:flex">
            <div className="flex items-center gap-2 rounded-lg border border-line bg-surface px-3 py-2 text-sm font-semibold"><Zap size={16} className="text-coral" /> {progress.score.toLocaleString()} <span className="font-normal text-ink/50">points</span></div>
            <div className="flex items-center gap-2 rounded-lg bg-mint/15 px-3 py-2 text-sm font-semibold text-mint-dark"><Flame size={16} /> {progress.streak} streak</div>
          </div>
        </div>
      </header>
      <div className="mx-auto flex max-w-[1440px]">
         <aside className="hidden border-line lg:static lg:block lg:w-64 lg:shrink-0 lg:border-r lg:p-8">
          <p className="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.2em] text-ink/40">Game room</p>
          <nav className="space-y-1">
             {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
               return <button key={item.id} onClick={() => setView(item.id)} className={cn("flex w-full items-center gap-3 rounded-lg px-3 py-3 text-left text-sm font-semibold transition-colors", view === item.id ? "bg-ink text-paper" : "text-ink/65 hover:bg-surface hover:text-ink")}><Icon size={18} /> {item.label}{view === item.id && <ChevronRight size={15} className="ml-auto" />}</button>;
            })}
          </nav>
          <div className="mt-10 border-t border-line pt-6">
            <div className="rounded-lg bg-surface p-4"><div className="mb-3 flex items-center justify-between"><span className="text-xs font-bold uppercase tracking-wider text-ink/50">Current level</span><span className="text-xs font-bold text-coral">{progress.unlockedLevel}/10</span></div><div className="h-2 overflow-hidden rounded-full bg-line"><div className="h-full rounded-full bg-coral transition-all" style={{ width: `${progress.unlockedLevel * 10}%` }} /></div><p className="mt-3 text-xs leading-relaxed text-ink/55">Win rounds to unlock tougher words and earn more points.</p></div>
          </div>
        </aside>
         <main className="min-w-0 flex-1 px-4 pb-28 pt-6 sm:px-5 sm:py-8 lg:px-10 lg:py-12">{renderView()}</main>
      </div>
       <nav aria-label="Game screens" className="fixed inset-x-0 bottom-0 z-30 border-t border-line bg-paper/95 px-2 pb-[max(0.65rem,env(safe-area-inset-bottom))] pt-2 backdrop-blur-lg lg:hidden">
         <div className="mx-auto grid max-w-lg grid-cols-5 gap-1">
           {NAV_ITEMS.map((item) => {
             const Icon = item.icon;
             const active = view === item.id;
             return <button key={item.id} onClick={() => setView(item.id)} aria-current={active ? "page" : undefined} className={cn("flex min-w-0 flex-col items-center gap-1 rounded-lg px-1 py-2 text-[10px] font-bold transition-colors", active ? "bg-ink text-paper" : "text-ink/45 hover:bg-surface hover:text-ink")}><Icon size={18} strokeWidth={active ? 2.5 : 2} /><span className="truncate">{item.label === "How to play" ? "How to play" : item.label}</span></button>;
           })}
         </div>
       </nav>
    </div>
  );
}

interface PlayViewProps {
  mode: Mode; themeName: string; level: (typeof LEVELS)[number]; word: string; revealedWord: string[]; guessed: Set<string>; wrongGuesses: number; maxChances: number; hintUsed: boolean; status: GameStatus; score: number; playerName: string;
  onModeChange: (mode: Mode) => void; onGuess: (letter: string) => void; onHint: () => void; onRestart: () => void;
}

function PlayView({ mode, themeName, level, word, revealedWord, guessed, wrongGuesses, maxChances, hintUsed, status, score, playerName, onModeChange, onGuess, onHint, onRestart }: PlayViewProps) {
  const message = status === "won" ? "You got it!" : status === "lost" ? "Round over" : "Choose a letter to begin";
  return <div className="mx-auto max-w-6xl animate-in fade-in duration-500">
     <div className="mb-6 flex flex-col justify-between gap-4 sm:mb-8 md:flex-row md:items-end"><div><p className="mb-2 text-xs font-bold uppercase tracking-[0.2em] text-coral">Welcome, {playerName}</p><h1 className="font-display text-3xl font-bold tracking-tight text-ink sm:text-5xl">Ready to guess?</h1><p className="mt-3 max-w-xl text-sm leading-6 text-ink/55 sm:text-base">A fresh word is waiting. Keep your guesses sharp and save the stick figure.</p></div></div>
    <div className="mb-6 flex flex-wrap gap-2">{(["Classic", "Survival", "Random", "Challenge"] as Mode[]).map((item) => <button key={item} onClick={() => onModeChange(item)} className={cn("rounded-lg border px-4 py-2 text-sm font-semibold transition-colors", mode === item ? "border-ink bg-ink text-paper" : "border-line bg-surface text-ink/60 hover:border-ink/40 hover:text-ink")}>{item}</button>)}</div>
     <div className="grid gap-5 xl:grid-cols-[minmax(0,1.5fr)_minmax(320px,0.85fr)]">
       <section className="rounded-lg border border-line bg-surface p-4 shadow-[0_18px_50px_-32px_var(--shadow)] sm:p-8">
        <div className="mb-7 flex flex-wrap items-center justify-between gap-3 border-b border-line pb-5"><div className="flex items-center gap-3"><span className="flex h-11 w-11 items-center justify-center rounded-lg bg-coral/12 text-2xl">{THEMES.find((theme) => theme.name === themeName)?.icon ?? "🎲"}</span><div><p className="text-xs font-bold uppercase tracking-widest text-ink/40">Theme</p><p className="font-display text-lg font-bold">{themeName}</p></div></div><div className="text-right"><p className="text-xs font-bold uppercase tracking-widest text-ink/40">Level {level.number}</p><p className="font-semibold text-coral">{level.name}</p></div></div>
         <div className="grid items-center gap-6 md:grid-cols-[220px_1fr]"><HangmanFigure wrongGuesses={wrongGuesses} maxChances={maxChances} status={status} /><div><p className="mb-3 text-center text-sm font-semibold text-ink/45 md:text-left">{message}</p><div className="flex flex-wrap justify-center gap-2 md:justify-start" aria-label="Word to guess">{revealedWord.map((letter, index) => <span key={`${index}-${letter}`} className={cn("flex h-12 min-w-9 items-center justify-center border-b-2 px-1 font-display text-2xl font-bold sm:h-14 sm:min-w-11 sm:text-3xl", letter === "_" ? "border-ink/20 text-ink/25" : "border-mint text-ink")}>{letter}</span>)}</div><div className="mt-6 flex flex-wrap items-center justify-center gap-3 md:justify-start"><span className={cn("rounded-full px-3 py-1 text-xs font-bold", wrongGuesses >= maxChances - 1 ? "bg-coral/12 text-coral" : "bg-mint/12 text-mint-dark")}>{maxChances - wrongGuesses} chances left</span>{hintUsed && <span className="rounded-full bg-yellow/20 px-3 py-1 text-xs font-bold text-yellow-dark">Hint used · -{HINT_COST}</span>}</div>{status !== "playing" && <div className={cn("mt-6 rounded-lg p-4 text-center md:text-left", status === "won" ? "bg-mint/12" : "bg-coral/10")}><p className="font-display text-lg font-bold">{status === "won" ? `+${BASE_WIN_SCORE + level.scoreBonus * 10} points earned` : "The hangman is out of chances"}</p><p className="mt-1 text-sm text-ink/55">{status === "won" ? "Great round. Keep your streak alive." : "The word stays hidden. Start a new round and try again."}</p><Button onClick={onRestart} className="mt-3" size="sm"><RotateCcw size={15} /> New word</Button></div>}</div></div>
      </section>
       <section className="rounded-lg border border-line bg-ink p-4 text-paper shadow-[0_18px_50px_-32px_var(--shadow)] sm:p-7"><div className="mb-5 flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-widest text-paper/45">Your score</p><p className="mt-1 font-display text-3xl font-bold sm:text-4xl">{score.toLocaleString()}</p></div><span className="flex h-10 w-10 items-center justify-center rounded-lg bg-paper/10 text-yellow"><Trophy size={20} /></span></div><p className="mb-3 text-xs font-bold uppercase tracking-widest text-paper/45">Guesses</p><div className="grid grid-cols-7 gap-1.5 sm:gap-2">{LETTERS.map((letter) => { const isGuessed = guessed.has(letter); const isCorrect = isGuessed && word.includes(letter); return <button key={letter} disabled={isGuessed || status !== "playing"} onClick={() => onGuess(letter)} aria-label={`Guess ${letter}`} className={cn("aspect-square rounded-md text-xs font-bold transition-all sm:text-sm", !isGuessed && status === "playing" ? "bg-paper/10 text-paper hover:bg-coral hover:text-paper" : isCorrect ? "bg-mint text-ink" : "bg-paper/8 text-paper/25")}>{letter}</button>; })}</div><div className="mt-6 flex items-center justify-between gap-3 border-t border-paper/15 pt-4"><div className="flex min-w-0 items-center gap-2"><Lightbulb size={17} className="shrink-0 text-yellow" /><div className="min-w-0"><p className="text-sm font-semibold">Need a clue?</p><p className="truncate text-xs text-paper/45">Reveal a letter for {HINT_COST} points</p></div></div><Button variant="secondary" size="sm" onClick={onHint} disabled={hintUsed || score < HINT_COST || status !== "playing"}><Gift size={15} /> Hint</Button></div></section>
    </div>
  </div>;
}

function HangmanFigure({ wrongGuesses, maxChances, status }: { wrongGuesses: number; maxChances: number; status: GameStatus }) {
  const partCount = maxChances === MAX_WRONG ? wrongGuesses : Math.ceil((wrongGuesses / maxChances) * MAX_WRONG);
  const isDead = status === "lost" && partCount >= MAX_WRONG;
  return (
    <div className="mx-auto flex w-full max-w-[220px] flex-col items-center">
      <svg
        viewBox="0 0 220 240"
        className={cn("h-auto w-full", isDead ? "text-coral" : "text-ink")}
        role="img"
        aria-label={isDead ? "Hangman has lost the round" : `${wrongGuesses} of ${maxChances} wrong guesses`}
      >
        <path d="M36 218h144M60 218V25h92M60 25h82M142 25v31" fill="none" stroke="currentColor" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
        {partCount >= 1 && <circle cx="142" cy="78" r="22" fill="none" stroke="currentColor" strokeWidth="6" className="hangman-pop" />}
        {partCount >= 2 && <path d="M142 100v62" fill="none" stroke="currentColor" strokeWidth="6" strokeLinecap="round" />}
        {partCount >= 3 && <path d="M142 116l-31 28" fill="none" stroke="currentColor" strokeWidth="6" strokeLinecap="round" />}
        {partCount >= 4 && <path d="M142 116l31 28" fill="none" stroke="currentColor" strokeWidth="6" strokeLinecap="round" />}
        {partCount >= 5 && <path d="M142 162l-28 39" fill="none" stroke="currentColor" strokeWidth="6" strokeLinecap="round" />}
        {partCount >= 6 && <path d="M142 162l28 39M134 71l-6 6m6 0-6-6m22 0-6 6m6 0-6-6M132 89q10-8 20 0" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" />}
      </svg>
      <div className="mt-2 flex w-full gap-1" aria-hidden="true">
        {Array.from({ length: maxChances }, (_, index) => (
          <span key={index} className={cn("h-1.5 flex-1 rounded-full", index < wrongGuesses ? "bg-coral" : "bg-ink/10")} />
        ))}
      </div>
    </div>
  );
}

function ThemesView({ selectedTheme, onSelect }: { selectedTheme: number; onSelect: (index: number) => void }) {
  return <ContentHeader eyebrow="Choose your arena" title="Themes" description="Every theme brings a new vocabulary to the guessing board."><div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{THEMES.map((theme, index) => <button key={theme.name} onClick={() => onSelect(index)} className={cn("group flex items-center gap-4 rounded-lg border bg-surface p-5 text-left transition-all hover:-translate-y-0.5 hover:border-ink/40 hover:shadow-lg", selectedTheme === index ? "border-coral ring-1 ring-coral" : "border-line")}><span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-paper text-2xl">{theme.icon}</span><span className="min-w-0"><span className="block font-display font-bold">{theme.name}</span><span className="mt-1 block text-xs text-ink/50">{theme.words.length} words to discover</span></span><ChevronRight size={17} className="ml-auto text-ink/25 transition-transform group-hover:translate-x-1" /></button>)}</div></ContentHeader>;
}

function LevelsView({ unlockedLevel, selectedLevel, onSelect }: { unlockedLevel: number; selectedLevel: number; onSelect: (level: number) => void }) {
  return <ContentHeader eyebrow="Climb the ladder" title="Levels" description="The longer the word, the bigger the reward. Win to unlock what comes next."><div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">{LEVELS.map((level) => { const locked = level.number > unlockedLevel; return <button key={level.number} disabled={locked} onClick={() => onSelect(level.number)} className={cn("relative rounded-lg border p-5 text-left transition-all", locked ? "cursor-not-allowed border-line bg-paper/60 text-ink/35" : selectedLevel === level.number ? "border-coral bg-surface ring-1 ring-coral" : "border-line bg-surface hover:-translate-y-0.5 hover:border-ink/40")}><span className="flex items-center justify-between"><span className="font-display text-2xl font-bold">{String(level.number).padStart(2, "0")}</span>{locked ? <Lock size={17} /> : selectedLevel === level.number ? <Check size={18} className="text-coral" /> : <ChevronRight size={17} />}</span><span className="mt-5 block font-semibold">{level.name}</span><span className="mt-1 block text-xs">Up to {level.maxLength > 20 ? "any length" : `${level.maxLength} letters`} · +{level.scoreBonus * 10} bonus</span></button>; })}</div></ContentHeader>;
}

function StatisticsView({ progress, accuracy }: { progress: Progress; accuracy: number }) {
  const stats = [["Rounds played", progress.rounds, Gamepad2], ["Words solved", progress.wins, Check], ["Best streak", progress.bestStreak, Flame], ["Best round", progress.bestScore, Trophy]] as const;
  return <ContentHeader eyebrow="Your record" title="Statistics" description="A quick look at how you are progressing through the word board."><div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{stats.map(([label, value, Icon]) => <div key={label} className="rounded-lg border border-line bg-surface p-5"><Icon size={19} className="text-coral" /><p className="mt-6 font-display text-3xl font-bold">{value.toLocaleString()}</p><p className="mt-1 text-sm text-ink/50">{label}</p></div>)}</div><div className="mt-6 grid gap-6 lg:grid-cols-2"><div className="rounded-lg border border-line bg-surface p-6"><div className="flex items-center justify-between"><span className="font-semibold">Win rate</span><span className="font-display text-2xl font-bold text-mint-dark">{accuracy}%</span></div><div className="mt-5 h-3 overflow-hidden rounded-full bg-line"><div className="h-full rounded-full bg-mint transition-all" style={{ width: `${accuracy}%` }} /></div><p className="mt-4 text-sm text-ink/50">{progress.wins} wins from {progress.rounds} completed rounds.</p></div><div className="rounded-lg border border-line bg-surface p-6"><div className="flex items-center gap-2"><Shield size={19} className="text-coral" /><span className="font-semibold">Achievements</span></div><p className="mt-4 font-display text-3xl font-bold">{progress.achievements.length}<span className="ml-1 text-base font-normal text-ink/40">/ {ACHIEVEMENTS.length}</span></p><p className="mt-1 text-sm text-ink/50">Badges collected so far</p><div className="mt-4 flex gap-1">{ACHIEVEMENTS.map((achievement) => <span key={achievement.id} title={achievement.name} className={cn("h-2 flex-1 rounded-full", progress.achievements.includes(achievement.id) ? "bg-yellow" : "bg-line")} />)}</div></div></div></ContentHeader>;
}

function HowToPlayView() {
  const steps = [["Pick a mode", "Classic is the standard round. Try Survival, Random, or Challenge when you want a twist."], ["Reveal the word", "Choose letters from the board. Correct guesses fill in every matching spot."], ["Protect your chances", "Each wrong letter adds another part to the hangman. Six mistakes ends a Classic round."], ["Spend hints wisely", `A hint reveals one letter and costs ${HINT_COST} points. A clean solve earns the biggest bonus.`]];
  return <ContentHeader eyebrow="The rules" title="How to play" description="Simple rules, satisfying wins. Jump into a round whenever you are ready."><div className="grid gap-4 md:grid-cols-2">{steps.map(([title, description], index) => <div key={title} className="rounded-lg border border-line bg-surface p-6"><span className="flex h-9 w-9 items-center justify-center rounded-lg bg-coral text-sm font-bold text-paper">0{index + 1}</span><h2 className="mt-6 font-display text-xl font-bold">{title}</h2><p className="mt-2 text-sm leading-6 text-ink/55">{description}</p></div>)}</div><div className="mt-6 rounded-lg bg-ink p-6 text-paper"><div className="flex items-center gap-3"><Sparkles className="text-yellow" size={20} /><p className="font-display text-lg font-bold">The golden rule</p></div><p className="mt-3 max-w-2xl text-sm leading-6 text-paper/60">Think before you guess. Repeated letters do not cost a chance, and every solved word helps open the next level.</p></div></ContentHeader>;
}

function ContentHeader({ eyebrow, title, description, children }: { eyebrow: string; title: string; description: string; children: React.ReactNode }) {
  return <div className="mx-auto max-w-6xl animate-in fade-in duration-500"><div className="mb-9"><p className="mb-2 text-xs font-bold uppercase tracking-[0.2em] text-coral">{eyebrow}</p><h1 className="font-display text-4xl font-bold tracking-tight text-ink sm:text-5xl">{title}</h1><p className="mt-3 max-w-xl text-base text-ink/55">{description}</p></div>{children}</div>;
}
