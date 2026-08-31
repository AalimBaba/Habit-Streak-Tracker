import HabitForm from './HabitForm'
import HabitCard from './HabitCard'
import { startOfTodayISO } from '../utils/date'

export default function HabitList({ habits, setHabits }) {
  const today = startOfTodayISO()

  const addHabit = (habit) => {
    setHabits((current) => [...current, habit])
  }

  const patchHabit = (id, patch) => {
    setHabits((current) => current.map((habit) => (habit.id === id ? { ...habit, ...patch } : habit)))
  }

  const removeHabit = (id) => {
    setHabits((current) => current.filter((habit) => habit.id !== id))
  }

  return (
    <section className="space-y-4">
      <HabitForm onAdd={addHabit} />

      {habits.length === 0 ? (
        <div className="card p-5 text-sm text-gray-300">No habits yet. Add one above to start your streak.</div>
      ) : (
        <div className="grid gap-3">
          {habits.map((habit) => (
            <HabitCard
              key={habit.id}
              habit={habit}
              onToggleToday={(checked) => {
                const history = new Set(habit.history || [])
                if (checked) {
                  history.add(today)
                } else {
                  history.delete(today)
                }
                patchHabit(habit.id, { history: Array.from(history).sort() })
              }}
              onRename={(title) => patchHabit(habit.id, { title })}
              onDelete={() => removeHabit(habit.id)}
            />
          ))}
        </div>
      )}
    </section>
  )
}
