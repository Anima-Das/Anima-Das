"""Rebuild the hand-authored root-level SVG assets in this flat-upload package."""
from pathlib import Path
import design_source__hero as hero
import design_source__parts as parts
from design_source__lib import CYAN, VIOLET, AMBER

ROOT = Path(__file__).resolve().parent
def write(name, content):
    (ROOT / name).write_text(content, encoding="utf-8")

write("assets__hero.svg", hero.build())
for card in parts.CARDS:
    write(f"assets__cards__{card['file']}.svg", parts.card(card))
for card in parts.ALSO:
    write(f"assets__cards__{card['file']}.svg", parts.card(card, w=480, h=214, full=False))
write("assets__stack.svg", parts.stack())
write("assets__pipeline.svg", parts.pipeline())
write("assets__links__linkedin.svg", parts.button("LinkedIn", CYAN, 150))
write("assets__links__email.svg", parts.button("Email", VIOLET, 126))
write("assets__links__website.svg", parts.button("Portfolio site", AMBER, 170))
write("assets__links__status.svg", parts.status())
write("assets__divider.svg", parts.divider())
write("assets__footer.svg", parts.footer())
print("Flat SVG assets rebuilt")
