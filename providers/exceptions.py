class ExceptionSearchingNetworkError(Exception):

    def __init__(self, resource: str, raw_anime_name: str, provider_name: str):
        super().__init__()
        self.resource = resource
        self.raw_anime_name = raw_anime_name
        self.provider_name = provider_name

    def __str__(self) -> str:
        return f"Couldn't get {self.resource} for {self.raw_anime_name} from {self.provider_name}"
