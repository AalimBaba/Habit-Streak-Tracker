import { useMemo, useState } from 'react'
import { computeStreaks, lastNDaysArray, startOfTodayISO } from '../utils/date'

export default function HabitCard({ habit, onToggleToday, onDelete, onRename }) {
  const [editing, setEditing] = useState(false)
  const [name, setName] = useState(habit.title)

  const today = startOfTodayISO()
  const doneToday = (habit.history || []).includes(today)
  const streaks = useMemo(() => computeStreaks(habit.history || [], today), [habit.history, today])
  const history7 = useMemo(() => lastNDaysArray(7, today), [today])

  const saveName = () => {
    const next = name.trim()
    if (next && next !== habit.title) {
      onRename(next)
    }
    setEditing(false)
    setName(next || habit.title)
  }

  return (
    <article className={`card p-4 transition ${doneToday ? 'neon-border' : ''}`}>
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          {editing ? (
            <input
              value={name}
              onChange={(event) => setName(event.target.value)}
              onBlur={saveName}
              onKeyDown={(event) => {
                if (event.key === 'Enter') {
                  event.preventDefault()
                  saveName()
                }
              }}
              className="w-full rounded bg-black/35 px-2 py-1 text-sm outline-none ring-neon/40 focus:ring"
              autoFocus
              maxLength={60}
            />
          ) : (
            <h3 className="truncate text-base font-semibold">{habit.title}</h3>
          )}
          <p className="mt-1 text-xs text-gray-400">Current: {streaks.current} 🔥 · Best: {streaks.best} 🏆</p>
        </div>

        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={() => onToggleToday(!doneToday)}
            className={`rounded-md px-2 py-1 text-xs font-semibold transition ${doneToday ? 'bg-neon text-black' : 'bg-white/10 text-gray-200 hover:bg-white/20'}`}
          >
            {doneToday ? 'Done' : 'Mark'}
          </button>
          <button
            type="button"
            onClick={() => setEditing((current) => !current)}
            className="rounded-md bg-white/10 px-2 py-1 text-xs text-gray-200 hover:bg-white/20"
          >
            Edit
          </button>
          <button
            type="button"
            onClick={onDelete}
            className="rounded-md bg-red-500/20 px-2 py-1 text-xs text-red-300 hover:bg-red-500/30"
          >
            Delete
          </button>
        </div>
      </div>

      <div className="mt-3">
        <p className="mb-2 text-xs uppercase tracking-wide text-gray-400">Last 7 days</p>
        <div className="grid grid-cols-7 gap-1">
          {history7.map((date) => {
            const checked = (habit.history || []).includes(date)
            return (
              <div key={date} className="flex flex-col items-center gap-1">
                <span className="text-[10px] text-gray-400">{date.slice(5)}</span>
                <span
                  className={`h-6 w-6 rounded-md border text-center text-xs leading-6 ${checked ? 'border-neon bg-neon/20 text-neon' : 'border-white/15 text-gray-500'}`}
                  title={date}
                >
                  {checked ? '✓' : '·'}
                </span>
              </div>
            )
          })}
        </div>
      </div>
    </article>
  )
}
