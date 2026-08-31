import { useState } from 'react'
import { v4 as uuid } from 'uuid'
import { startOfTodayISO } from '../utils/date'

export default function HabitForm({ onAdd }) {
  const [name, setName] = useState('')

  const submit = (event) => {
    event.preventDefault()
    const title = name.trim()
    if (!title) return

    onAdd({
      id: uuid(),
      title,
      createdAt: startOfTodayISO(),
      history: []
    })

    setName('')
  }

  return (
    <form onSubmit={submit} className="card neon-border p-4 sm:p-5">
      <h2 className="text-lg font-semibold text-neon">Add a habit</h2>
      <div className="mt-3 flex flex-col gap-2 sm:flex-row">
        <input
          value={name}
          onChange={(event) => setName(event.target.value)}
          placeholder="e.g., 20 min workout"
          className="w-full rounded-lg border border-white/20 bg-black/30 px-3 py-2 text-sm outline-none ring-neon/40 placeholder:text-gray-400 focus:ring"
          maxLength={60}
        />
        <button
          type="submit"
          className="rounded-lg bg-neon px-4 py-2 text-sm font-semibold text-black transition hover:brightness-110"
        >
          Add
        </button>
      </div>
    </form>
  )
}
