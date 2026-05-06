"""Minimal local fallback for the webrtcvad module.

This keeps resemblyzer importable on systems where the native webrtcvad
extension cannot be built. The implementation is intentionally simple and
only aims to satisfy the small API surface used by resemblyzer.
"""

from __future__ import annotations

import audioop


class Vad:
    def __init__(self, mode: int = 0):
        self.set_mode(mode)

    def set_mode(self, mode: int) -> None:
        if mode not in (0, 1, 2, 3):
            raise ValueError("mode must be between 0 and 3")
        self.mode = mode

    def is_speech(self, pcm_data: bytes, sample_rate: int) -> bool:
        if sample_rate not in (8000, 16000, 32000, 48000):
            raise ValueError("sample_rate must be 8000, 16000, 32000, or 48000")
        if not pcm_data:
            return False

        rms = audioop.rms(pcm_data, 2)
        threshold = 500 - (self.mode * 75)
        return rms >= threshold
