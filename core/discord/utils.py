DISCORD_EPOCH = 1420070400000


def snowflake_epoch(snowflake: int) -> float:
    """ Convert snowflake to epoch timestamp

    Args:
        snowflake (int): snowflake to convert

    Returns:
        int: epoch timestamp converted from snowflake
    """
    return (snowflake >> 22) + DISCORD_EPOCH
