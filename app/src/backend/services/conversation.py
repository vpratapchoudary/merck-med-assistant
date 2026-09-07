from threading import Lock


class ConversationStore:
    """Process-local conversation history keyed by a client session ID."""

    def __init__(self) -> None:
        self._histories: dict[str, list[dict[str, str]]] = {}
        self._lock = Lock()

    def get(self, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            return list(self._histories.get(session_id, []))

    def append(
        self,
        session_id: str,
        user_message: str,
        assistant_message: str,
    ) -> None:
        with self._lock:
            history = self._histories.setdefault(session_id, [])
            history.extend(
                [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": assistant_message},
                ]
            )


conversation_store = ConversationStore()