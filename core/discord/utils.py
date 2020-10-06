DISCORD_EPOCH = 1420070400000


def snowflake_epoch(snowflake: int) -> int:
    return (snowflake >> 22) + DISCORD_EPOCH
