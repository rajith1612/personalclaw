import threading
import time
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class Heartbeat:

    def __init__(self, agent, get_skills_fn):
        self.agent = agent
        self.get_skills = get_skills_fn
        self._thread = None
        self._stop_event = threading.Event()
        self._running = False
        self.logs = []

    @property
    def running(self):
        return self._running

    def start(self):
        if self._running:
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        self._running = True
        self._log("Heartbeat started")

    def stop(self):
        if not self._running:
            return
        self._stop_event.set()
        self._running = False
        self._log("Heartbeat stopped")

    def _loop(self):
        skill_timers = {}

        while not self._stop_event.is_set():
            skills = self.get_skills()

            for skill in skills:
                name = skill["name"]
                interval = skill.get("schedule", 60) * 60
                last_run = skill_timers.get(name, 0)
                now = time.time()

                if now - last_run >= interval:
                    self._run_skill(skill)
                    skill_timers[name] = now

            self._stop_event.wait(timeout=30)

    def _run_skill(self, skill):
        name = skill["name"]
        prompt = skill.get("prompt", "")
        if not prompt:
            return

        self._log(f"Running skill: {name}")
        try:
            response = self.agent.run(prompt)
            self._log(f"Skill '{name}' completed: {response[:200]}")
        except Exception as e:
            self._log(f"Skill '{name}' failed: {e}")

    def _log(self, message):
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self.logs.append(entry)
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]
        logger.info(message)
