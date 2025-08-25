def parse_count(count_str: str) -> int:
    """
    Convert TikTok-style count strings to integer.
    Examples:
    - '48.7K' -> 48700
    - '67.1M' -> 67100000
    - '9818'  -> 9818
    """
    count_str = count_str.strip().upper()
    multiplier = 1

    if count_str.endswith("K"):
        multiplier = 1_000
        count_str = count_str[:-1]
    elif count_str.endswith("M"):
        multiplier = 1_000_000
        count_str = count_str[:-1]
    elif count_str.endswith("B"):
        multiplier = 1_000_000_000
        count_str = count_str[:-1]

    try:
        return int(float(count_str) * multiplier)
    except ValueError:
        return 0


def format_count(count_int: int) -> str:
    """
    Convert integers to TikTok-style readable counts.
    Examples:
    - 48700 -> '48.7K'
    - 67100000 -> '67.1M'
    - 9818 -> '9.8K'
    """
    if count_int >= 1_000_000_000:
        return f"{count_int / 1_000_000_000:.1f}B"
    elif count_int >= 1_000_000:
        return f"{count_int / 1_000_000:.1f}M"
    elif count_int >= 1_000:
        return f"{count_int / 1_000:.1f}K"
    else:
        return str(count_int)


if __name__ =="__main__":
    print("converting to int figure: ",parse_count("78.1M"))

    print("Converting to string: ", format_count(678000))

