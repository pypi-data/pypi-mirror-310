import enum


class Environment(enum.Enum):
    LIVE = "https://slack.com/api"
    MOCK_SERVER = "https://api.sideko-staging.dev/v1/mock/demo/simple-slack/0.2.0"
