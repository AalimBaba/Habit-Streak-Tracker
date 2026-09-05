/*
Reference logic:
- A streak increases by 1 for each consecutive day marked "done".
- A missed day (or unmarked past day) breaks the streak and resets the current run.
- Best streak is the highest historical consecutive run and should persist.
- Completion rate is done days divided by expected trackable days.
*/

/*
Data model and algorithm:
- Habit object: { id, name, createdAt, checkIns } where checkIns is a map of YYYY-MM-DD -> "done" | "missed".
- For historical calculations, days before today without a check-in are treated as "missed".
- Current streak scans backward from today (skipping today only if unmarked) until first non-done day.
- Best streak scans from createdAt to today, counting consecutive done days and resetting on non-done.
*/

const STORAGE_KEY = 'habit-streak-tracker-v1';
const DAYS_IN_HEATMAP = 30;

const state = {
  habits: loadHabits(),
};

const habitForm = document.getElementById('habit-form');
const habitInput = document.getElementById('habit-name');
const habitList = document.getElementById('habit-list');
const emptyState = document.getElementById('empty-state');
const habitCount = document.getElementById('habit-count');
const habitTemplate = document.getElementById('habit-template');

habitForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const name = habitInput.value.trim();
  if (!name) return;

  state.habits.unshift({
    id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random()),
    name,
    createdAt: todayISO(),
    checkIns: {},
  });

  habitInput.value = '';
  saveHabits();
  render();
});

function loadHabits() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed
      .filter((habit) => habit && typeof habit === 'object' && habit.id && habit.name)
      .map((habit) => ({
        id: String(habit.id),
        name: String(habit.name),
        createdAt: normalizeISO(habit.createdAt) || todayISO(),
        checkIns: sanitizeCheckIns(habit.checkIns),
      }));
  } catch {
    return [];
  }
}

function sanitizeCheckIns(input) {
  if (!input || typeof input !== 'object') return {};
  const out = {};
  for (const [date, status] of Object.entries(input)) {
    if (/^\d{4}-\d{2}-\d{2}$/.test(date) && (status === 'done' || status === 'missed')) {
      out[date] = status;
    }
  }
  return out;
}

function saveHabits() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.habits));
}

function render() {
  habitList.innerHTML = '';
  const count = state.habits.length;
  habitCount.textContent = `${count} ${count === 1 ? 'habit' : 'habits'}`;
  emptyState.hidden = count !== 0;

  state.habits.forEach((habit) => {
    const node = habitTemplate.content.firstElementChild.cloneNode(true);

    node.querySelector('.habit__name').textContent = habit.name;

    const metrics = getMetrics(habit);
    node.querySelector('.stat-current').textContent = String(metrics.currentStreak);
    node.querySelector('.stat-best').textContent = String(metrics.bestStreak);
    node.querySelector('.stat-rate').textContent = `${metrics.completionRate}%`;
    node.querySelector('.coach-message').textContent = getCoachMessage(habit, metrics);

    node.querySelector('.done-btn').addEventListener('click', () => {
      setCheckIn(habit.id, todayISO(), 'done');
    });

    node.querySelector('.missed-btn').addEventListener('click', () => {
      setCheckIn(habit.id, todayISO(), 'missed');
    });

    node.querySelector('.clear-btn').addEventListener('click', () => {
      clearCheckIn(habit.id, todayISO());
    });

    node.querySelector('.remove-btn').addEventListener('click', () => {
      state.habits = state.habits.filter((item) => item.id !== habit.id);
      saveHabits();
      render();
    });

    const heatmap = node.querySelector('.heatmap');
    getLastNDates(DAYS_IN_HEATMAP).forEach((date) => {
      const day = document.createElement('button');
      day.type = 'button';
      day.className = 'day';
      if (date === todayISO()) day.classList.add('today');
      day.dataset.status = getStoredStatus(habit, date) || 'none';
      day.title = `${date}: ${day.dataset.status}`;

      day.addEventListener('click', () => {
        const next = cycleStatus(getStoredStatus(habit, date));
        if (!next) {
          clearCheckIn(habit.id, date);
        } else {
          setCheckIn(habit.id, date, next);
        }
      });

      heatmap.appendChild(day);
    });

    habitList.appendChild(node);
  });
}

function cycleStatus(status) {
  if (status === 'done') return 'missed';
  if (status === 'missed') return undefined;
  return 'done';
}

function setCheckIn(habitId, date, status) {
  const habit = state.habits.find((item) => item.id === habitId);
  if (!habit) return;
  habit.checkIns[date] = status;
  saveHabits();
  render();
}

function clearCheckIn(habitId, date) {
  const habit = state.habits.find((item) => item.id === habitId);
  if (!habit) return;
  delete habit.checkIns[date];
  saveHabits();
  render();
}

function getStoredStatus(habit, date) {
  return habit.checkIns[date];
}

function getEffectiveStatus(habit, date) {
  const stored = getStoredStatus(habit, date);
  if (stored) return stored;
  if (date < todayISO()) return 'missed';
  return undefined;
}

function getMetrics(habit) {
  const currentStreak = getCurrentStreak(habit);
  const bestStreak = getBestStreak(habit);
  const completionRate = getCompletionRate(habit);
  return { currentStreak, bestStreak, completionRate };
}

function getCurrentStreak(habit) {
  let streak = 0;
  let date = todayISO();

  if (!getStoredStatus(habit, date)) {
    date = shiftISO(date, -1);
  }

  while (date >= habit.createdAt) {
    if (getEffectiveStatus(habit, date) !== 'done') break;
    streak += 1;
    date = shiftISO(date, -1);
  }

  return streak;
}

function getBestStreak(habit) {
  let best = 0;
  let run = 0;
  let date = habit.createdAt;

  while (date <= todayISO()) {
    if (getEffectiveStatus(habit, date) === 'done') {
      run += 1;
      if (run > best) best = run;
    } else {
      run = 0;
    }
    date = shiftISO(date, 1);
  }

  return best;
}

function getCompletionRate(habit) {
  const end = getStoredStatus(habit, todayISO()) ? todayISO() : shiftISO(todayISO(), -1);
  if (end < habit.createdAt) return 0;

  let done = 0;
  let total = 0;
  let date = habit.createdAt;

  while (date <= end) {
    total += 1;
    if (getEffectiveStatus(habit, date) === 'done') {
      done += 1;
    }
    date = shiftISO(date, 1);
  }

  return total ? Math.round((done / total) * 100) : 0;
}

function getCoachMessage(habit, metrics) {
  const today = todayISO();
  const yesterday = shiftISO(today, -1);
  const todayStatus = getStoredStatus(habit, today);
  const yesterdayStatus = getEffectiveStatus(habit, yesterday);

  if (metrics.currentStreak > 0 && metrics.currentStreak === metrics.bestStreak && metrics.bestStreak > 1) {
    return `🔥 New record streak (${metrics.currentStreak}) — keep it going!`;
  }

  if (todayStatus === 'missed') {
    return 'A miss today reset your streak. Restart with one small win now.';
  }

  if (!todayStatus && yesterdayStatus === 'done' && metrics.currentStreak > 0) {
    return `⚠️ Streak at risk (${metrics.currentStreak}). Mark today done to protect it.`;
  }

  if (yesterdayStatus === 'missed') {
    return 'You missed yesterday — today is a great reset point.';
  }

  if (todayStatus === 'done') {
    return 'Nice work! Today is locked in.';
  }

  return 'Start small today and build consistency.';
}

function getLastNDates(n) {
  const dates = [];
  let date = shiftISO(todayISO(), -(n - 1));
  for (let i = 0; i < n; i += 1) {
    dates.push(date);
    date = shiftISO(date, 1);
  }
  return dates;
}

function normalizeISO(value) {
  if (typeof value !== 'string') return null;
  return /^\d{4}-\d{2}-\d{2}$/.test(value) ? value : null;
}

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

function shiftISO(isoDate, days) {
  const date = new Date(`${isoDate}T00:00:00Z`);
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().slice(0, 10);
}

render();
