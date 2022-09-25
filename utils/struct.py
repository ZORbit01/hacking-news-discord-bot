from hackernews import HackerNews


class HackerNewsPrev(HackerNews):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_news = None

    def get_latest_news(self):
        return super().last_newstories()
