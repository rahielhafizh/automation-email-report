from dataclasses import dataclass
from datetime import datetime
from pynput import mouse, keyboard


@dataclass
class ClickRecord:
    x: int
    y: int
    button: str
    timestamp: str


class CursorRecorder:
    def __init__(self) -> None:
        self.records: list[ClickRecord] = []
        self._mouse_listener: mouse.Listener | None = None
        self._keyboard_listener: keyboard.Listener | None = None

    def _on_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        if not pressed:
            return

        record = ClickRecord(
            x=x,
            y=y,
            button=button.name,
            timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3],
        )
        self.records.append(record)
        print(
            f"[CLICK] #{len(self.records)} -> X: {x}, Y: {y} ({button.name}) at {record.timestamp}"
        )

    def _on_press(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        if key == keyboard.Key.space:
            self._stop()

    def _stop(self) -> None:
        if self._mouse_listener:
            self._mouse_listener.stop()
        if self._keyboard_listener:
            self._keyboard_listener.stop()

    def start(self) -> None:
        print("[SYSTEM] RECORDING STARTED - PRESS SPACE TO STOP")
        self._mouse_listener = mouse.Listener(on_click=self._on_click)
        self._keyboard_listener = keyboard.Listener(on_press=self._on_press)
        self._mouse_listener.start()
        self._keyboard_listener.start()
        self._mouse_listener.join()
        self._keyboard_listener.join()
        self._print_summary()

    def _print_summary(self) -> None:
        print("\n" + "=" * 50)
        print(f"[SUMMARY] TOTAL CLICKS RECORDED: {len(self.records)}")
        print("=" * 50)

        if not self.records:
            print("[SUMMARY] NO CLICKS WERE RECORDED")
            return

        for index, record in enumerate(self.records, start=1):
            print(
                f"{index:>3}. X: {record.x:>5}  Y: {record.y:>5}  BUTTON: {record.button:<6} TIME: {record.timestamp}"
            )

        print("\n[SUMMARY] UNIQUE COORDINATES:")
        unique_coords = sorted({(r.x, r.y) for r in self.records})
        for x, y in unique_coords:
            print(f"  -> X: {x}, Y: {y}")


def main() -> None:
    recorder = CursorRecorder()
    recorder.start()


if __name__ == "__main__":
    main()
