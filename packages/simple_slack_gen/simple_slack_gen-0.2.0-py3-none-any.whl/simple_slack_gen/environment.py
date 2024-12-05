import enum


class Environment(enum.Enum):
    LIVE = "https://slack.com/api"
    MOCK_SERVER = "http://127.0.0.1:8082/v1/mock/elias-local/slack/0.0.2"
