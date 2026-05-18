import re
import yaml
from pathlib import Path


SKILLS_DIR = Path.home() / ".youropenclaw" / "skills"


def _parse_skill_file(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not match:
        return None
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    meta["prompt"] = match.group(2).strip()
    meta["file"] = path.name
    meta.setdefault("enabled", True)
    meta.setdefault("schedule", 60)
    return meta


def _write_skill_file(path, meta, prompt):
    frontmatter = {
        "name": meta["name"],
        "description": meta.get("description", ""),
        "schedule": meta.get("schedule", 60),
        "enabled": meta.get("enabled", True),
    }
    content = "---\n" + yaml.dump(frontmatter, default_flow_style=False).strip() + "\n---\n\n" + prompt + "\n"
    path.write_text(content, encoding="utf-8")


def list_skills():
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    skills = []
    for f in sorted(SKILLS_DIR.glob("*.md")):
        skill = _parse_skill_file(f)
        if skill:
            skills.append(skill)
    return skills


def get_enabled_skills():
    return [s for s in list_skills() if s.get("enabled", True)]


def create_skill(name, description, prompt, schedule=60, enabled=True):
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    filename = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + ".md"
    path = SKILLS_DIR / filename
    meta = {
        "name": name,
        "description": description,
        "schedule": schedule,
        "enabled": enabled,
    }
    _write_skill_file(path, meta, prompt)
    return filename


def toggle_skill(filename, enabled):
    path = SKILLS_DIR / filename
    if not path.exists():
        return False
    skill = _parse_skill_file(path)
    if not skill:
        return False
    skill["enabled"] = enabled
    _write_skill_file(path, skill, skill["prompt"])
    return True


def delete_skill(filename):
    path = SKILLS_DIR / filename
    if path.exists():
        path.unlink()
        return True
    return False
