export function toLocalISODate(date = new Date()) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export function startOfTodayISO() {
  return toLocalISODate(new Date())
}

export function parseISODate(iso) {
  const [year, month, day] = iso.split('-').map(Number)
  return new Date(year, month - 1, day)
}

export function addDaysLocal(iso, days) {
  const d = parseISODate(iso)
  d.setDate(d.getDate() + days)
  return toLocalISODate(d)
}

export function lastNDaysArray(n = 7, fromISO = startOfTodayISO()) {
  const days = []
  for (let i = n - 1; i >= 0; i -= 1) {
    days.push(addDaysLocal(fromISO, -i))
  }
  return days
}

export function computeStreaks(history = [], todayISO = startOfTodayISO()) {
  const unique = [...new Set(history)].sort()
  if (unique.length === 0) {
    return { current: 0, best: 0 }
  }

  const completed = new Set(unique)
  let current = 0
  let cursor = todayISO

  if (!completed.has(cursor)) {
    cursor = addDaysLocal(cursor, -1)
  }

  while (completed.has(cursor)) {
    current += 1
    cursor = addDaysLocal(cursor, -1)
  }

  let best = 0
  let run = 0
  for (let i = 0; i < unique.length; i += 1) {
    if (i === 0) {
      run = 1
    } else {
      run = addDaysLocal(unique[i - 1], 1) === unique[i] ? run + 1 : 1
    }
    if (run > best) {
      best = run
    }
  }

  return { current, best }
}
