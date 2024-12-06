from stfu_tg.md import MDOnlyElement


class HRuler(MDOnlyElement):
    def to_md(self) -> str:
        return '---'
