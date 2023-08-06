import enlighten

COLORS = [
    ("white_on_blue", "\033[94m"),
    ("black_on_green", "\033[92m"),
    ("white_on_purple", "\033[95m"),
    ("white_on_red", "\033[91m"),
    ("black_on_yellow", "\033[93m"),
    ("black_on_cyan", "\033[96m"),
]

END_COLOR = "\033[0m"


class LogContext:
    color_cache = {}

    def ctx_color(cls, ctx_id: str):
        if ctx_id not in cls.color_cache:
            cls.color_cache[ctx_id] = COLORS[len(cls.color_cache) % len(COLORS)]

        return cls.color_cache[ctx_id]

    def __init__(self, ctx_id: str):
        self.ctx_id = ctx_id
        self.color = self.ctx_color(ctx_id)

    def header(self, msg, *args):
        print(f"{self.color[1]}{str(msg).format(*args)}{END_COLOR}")

    def write(self, msg, *args):
        print(f"{self.color[1]}| {END_COLOR}{str(msg).format(*args)}")


class LogContextManager:
    def __init__(self):
        self.status_manager = enlighten.get_manager()
        self.status_cache = {}

    def set_context(
        self, ctx_id: str, commit_id: str, commit_message: str, status: str
    ) -> LogContext:
        logger = LogContext(ctx_id)
        if commit_message is None:
            commit_message_summary = ""
        else:
            commit_message_summary = commit_message.split("\n")[0][:70]
        if ctx_id not in self.status_cache:
            self.status_cache[ctx_id] = self.status_manager.status_bar(
                status_format="{status} [{commit_id}] - {commit_message}",
                color=logger.color[0],
                commit_id=(commit_id[:8] if commit_id else ""),
                commit_message=commit_message_summary,
                status=status,
                leave=False,
            )
        else:
            self.status_cache[ctx_id].update(
                commit_id=(commit_id[:8] if commit_id else ""),
                commit_message=commit_message_summary,
                status=status,
            )
        return logger

    def clear_context(self, ctx_id: str):
        if ctx_id in self.status_cache:
            self.status_cache[ctx_id].close(clear=True)
