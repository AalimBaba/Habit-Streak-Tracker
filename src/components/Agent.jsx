import { computeStreaks, startOfTodayISO } from '../utils/date'

const quotes = [
  'Small wins repeated daily become life-changing.',
  'Consistency beats intensity when intensity is rare.',
  'Progress is built in ordinary moments.',
  'Show up today, your future self is watching.'
]

export default function Agent({ habits }) {
  const hour = new Date().getHours()
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening'
  const today = startOfTodayISO()

  const completedToday = habits.filter((habit) => (habit.history || []).includes(today)).length
  const withSevenDayStreak = habits.filter((habit) => computeStreaks(habit.history || [], today).current >= 7)

  const quote = quotes[new Date().getDate() % quotes.length]

  let reaction = "Let's create your first habit and begin your streak journey."
  if (habits.length > 0 && completedToday === 0) {
    reaction = "No check-ins yet today. Start one now and I'll track the momentum."
  } else if (completedToday > 0) {
    reaction = `Great work—${completedToday} habit${completedToday > 1 ? 's are' : ' is'} complete today.`
  }
  if (withSevenDayStreak.length > 0) {
    reaction = `🎉 Celebration: ${withSevenDayStreak[0].title} reached a 7+ day streak!`
  }

  return (
    <aside className="card neon-border p-4 sm:p-5">
      <p className="text-sm text-neon">Tracer Agent</p>
      <h1 className="mt-1 text-xl font-bold">{greeting}! I'm your Habit Streak Tracer.</h1>
      <p className="mt-3 text-sm text-gray-200">{reaction}</p>
      <p className="mt-2 text-xs italic text-gray-400">“{quote}”</p>
    </aside>
  )
}
