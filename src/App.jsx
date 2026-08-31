import { useEffect, useMemo, useState } from 'react'
import HabitList from './components/HabitList'
import Agent from './components/Agent'
import useLocalStorage from './hooks/useLocalStorage'
import { startOfTodayISO } from './utils/date'

export default function App() {
  const [habits, setHabits] = useLocalStorage('hst:habits', [])
  const [lastReset, setLastReset] = useLocalStorage('hst:lastReset', startOfTodayISO())
  const [today, setToday] = useState(startOfTodayISO())

  useEffect(() => {
    const checkForNewDay = () => {
      const localToday = startOfTodayISO()
      setToday(localToday)
      if (lastReset !== localToday) {
        setLastReset(localToday)
      }
    }

    checkForNewDay()
    const timer = window.setInterval(checkForNewDay, 60 * 1000)
    return () => window.clearInterval(timer)
  }, [lastReset, setLastReset])

  const sortedHabits = useMemo(
    () => [...habits].sort((a, b) => a.title.localeCompare(b.title)),
    [habits, today]
  )

  return (
    <div className="min-h-screen bg-gradient-to-b from-midnight via-black to-midnight px-4 py-6 sm:px-6">
      <main className="mx-auto w-full max-w-4xl space-y-5">
        <Agent habits={sortedHabits} />
        <HabitList habits={sortedHabits} setHabits={setHabits} />
      </main>
    </div>
  )
}
