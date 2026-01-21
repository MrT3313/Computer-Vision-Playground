from PySide6.QtCore import QTimer, QObject, Signal
from typing import Optional


class PlaybackController(QObject):
    playback_state_changed = Signal(bool)
    
    def __init__(self, coordinator, speed_input):
        super().__init__()
        self._coordinator = coordinator
        self._speed_input = speed_input
        self._play_timer = QTimer()
        self._play_timer.setSingleShot(False)
        self._play_timer.timeout.connect(self._on_timer_timeout)
        self._update_interval()
    
    def _update_interval(self) -> None:
        speed = self._speed_input.value()
        interval_ms = int(speed * 1000)
        self._play_timer.setInterval(interval_ms)
    
    def start(self) -> None:
        if not self._coordinator:
            return
        
        from core import ApplicationState
        if self._coordinator.get_state() == ApplicationState.INITIAL:
            self._coordinator.start()
        
        self._update_interval()
        if not self._play_timer.isActive():
            self._play_timer.start()
            self.playback_state_changed.emit(True)
    
    def stop(self) -> None:
        if self._play_timer.isActive():
            self._play_timer.stop()
            self.playback_state_changed.emit(False)
    
    def is_playing(self) -> bool:
        return self._play_timer.isActive()
    
    def update_speed(self) -> None:
        was_active = self._play_timer.isActive()
        if was_active:
            self._play_timer.stop()
            self._update_interval()
            self._play_timer.start()
        else:
            self._update_interval()
    
    def _on_timer_timeout(self) -> None:
        if not self._coordinator:
            self.stop()
            return
        
        if self._coordinator.can_go_next():
            self._coordinator.next()
        else:
            self.stop()
