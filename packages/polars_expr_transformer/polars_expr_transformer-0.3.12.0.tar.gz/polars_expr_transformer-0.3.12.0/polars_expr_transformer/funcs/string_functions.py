import polars as pl
import polars_ds as pds
from typing import Dict
from polars_expr_transformer.funcs.utils import is_polars_expr, create_fix_col
from polars_expr_transformer.funcs.utils import PlStringType, PlIntType
from functools import partial


def concat(*columns) -> pl.Expr:
    """
    Concatenate the values of multiple columns into a single string.

    Parameters:
    - columns: List of columns to concatenate.

    Returns:
    - An expression representing the concatenated string.
    """
    columns = [create_fix_col(c) if not is_polars_expr(c) else c for c in columns]
    return pl.concat_str(columns)


def count_match(column: PlStringType, value: str) -> pl.Expr:

    """
    Count the number of occurrences of a given value in a column.

    Parameters:
    - column: The column in which to count the occurrences.
    - value: The value to count.

    Returns:
    - An expression representing the number of occurrences.
    """
    if isinstance(column, pl.Expr):
        return column.str.count_matches(value)
    return pl.lit(column).str.count_matches(value)


def length(column: PlStringType) -> pl.Expr:
    """
    Calculate the length of a given column or string.

    Parameters:
    - column: The column or string for which to calculate the length.

    Returns:
    - An expression representing the length.
    """
    if isinstance(column, str):
        return pl.lit(len(column))
    column: pl.Expr
    return column.str.len_chars()


def uppercase(text: PlStringType) -> pl.Expr:
    """
    Convert the characters in a given column or string to uppercase.

    Parameters:
    - text: The column or string to convert.

    Returns:
    - An expression representing the uppercase conversion.
    """
    if isinstance(text, pl.Expr):
        return text.str.to_uppercase()
    return pl.lit(text.__str__().upper())


def titlecase(text: PlStringType) -> pl.Expr:
    """
    Convert the characters in a given column or string to title case.

    Parameters:
    - text: The column or string to convert.

    Returns:
    - An expression representing the title case conversion.
    """
    if isinstance(text, pl.Expr):
        return text.str.to_titlecase()
    return pl.lit(text.__str__().title())


def to_string(text: PlStringType) -> pl.Expr:
    """
    Convert a given column or value to its string representation.

    Parameters:
    - text: The column or value to convert.

    Returns:
    - An expression representing the string conversion.
    """
    if isinstance(text, pl.Expr):
        return text.cast(str)
    return pl.lit(text.__str__())


def lowercase(text: PlStringType) -> pl.Expr:
    """
    Convert the characters in a given column or string to lowercase.

    Parameters:
    - text: The column or string to convert.

    Returns:
    - An expression representing the lowercase conversion.
    """
    if isinstance(text, pl.Expr):
        return text.str.to_lowercase()
    return pl.lit(text.__str__().lower())


def __left(row: Dict):
    v, l = row.values()
    if v is not None:
        return v[:l]
    return None


def left(column: PlStringType, length: pl.Expr | int) -> pl.Expr:
    """
    Extracts a substring from a column or string, starting from the beginning.

    Parameters:
    - column: The column or string from which to extract the substring.
    - length: The length of the substring to extract.

    Returns:
    - An expression representing the substring.
    """
    if is_polars_expr(column):
        if is_polars_expr(length):
            print(' pl.struct([column, length]).apply(lambda r: __left(r))')
            return pl.struct([column, length]).map_elements(lambda r: __left(r), return_dtype=pl.String)
        else:
            print('column.str.slice(0, length)')
            return column.str.slice(0, length)
    elif is_polars_expr(length):
        print('pl.struct([length]).apply(lambda r: column[:list(r.values)[0]])')
        return pl.struct([length]).map_elements(lambda r: column[:list(r.values)[0]], return_dtype=pl.String)
    else:
        print('pl.lit(column[:length])')
        return pl.lit(column[:length])


def __right(row: Dict):
    v, l = row.values()
    if v is not None:
        return v[-l:]


def right(column: PlStringType, length: PlIntType) -> pl.Expr:
    """
    Extracts a substring from a column or string, starting from the end.

    Parameters:
    - column: The column or string from which to extract the substring.
    - length: The length of the substring to extract.

    Returns:
    - An expression representing the substring.
    """

    if is_polars_expr(column):
        if is_polars_expr(length):
            return pl.struct([column, length]).map_elements(__right, return_dtype=pl.String)
        else:
            return column.str.slice(-length)
    elif is_polars_expr(length):
        return pl.struct([length]).map_elements(lambda r: column[-next(iter(r.values())):], return_dtype=pl.String)
    else:
        return pl.lit(column[-length:])


def __apply_replace(row, replace_by=None):
    v = list(row.values())
    main_str = v[0]
    other_str = v[1] if len(v) > 1 else None
    replace_str = v[2] if len(v) > 2 else replace_by
    return main_str.replace(other_str, replace_str)


def replace(main: PlStringType, other: PlStringType, replace_by: PlStringType) -> pl.Expr:
    """
       Replaces occurrences of a substring within a main string with another string.

       Parameters:
       - main: The main string or expression where the replacement will occur.
       - other: The substring or expression that needs to be replaced.
       - replace_by: The string or expression that will replace the 'other' substring in 'main'.

       Returns:
       An expression representing the string after replacement.

       Example:
       Given main = "Hello, world!", other = "world", and replace_by = "there"
       The function will return "Hello, there!"
       """
    if not is_polars_expr(main):
        main = pl.lit(main)
    return main.str.replace_all(other, replace_by, literal=True).cast(pl.Utf8)


def to_date(s: PlStringType, date_format: str = "%Y-%m-%d") -> pl.Expr:
    """
    Convert a string to a date.

    Parameters:
    - s (Any): The string to convert to a date. Can be a pl expression or any other value.
    - format (str): The format of the date string. Default is "%Y-%m-%d".

    Returns:
    - pl.Expr: A pl expression representing the converted date.

    Note: If `s` is not a pl expression, it will be converted into one.
    """
    s = s if is_polars_expr(s) else create_fix_col(s)
    return s.str.to_date(date_format, strict=False)


def to_datetime(s: PlStringType, date_format: str = "%Y-%m-%d %H:%M:%S") -> pl.Expr:
    """
    Convert a string to a datetime.

    Parameters:
    - s (Any): The string to convert to a datetime. Can be a pl expression or any other value.
    - format (str): The format of the datetime string. Default is "%Y-%m-%d %H:%M:%S".

    Returns:
    - pl.Expr: A pl expression representing the converted datetime.

    Note: If `s` is not a pl expression, it will be converted into one.
    """
    s = s if is_polars_expr(s) else create_fix_col(s)
    return s.str.to_datetime(date_format, strict=False)


def find_position(s: PlStringType, sub: PlStringType) -> pl.Expr:
    """
    Find the position of a substring within a string.

    Parameters:
    - s (Any): The string in which to find the position of the substring. Can be a pl expression or any other value.
    - sub (Any): The substring to find the position of. Can be a pl expression or any other value.

    Returns:
    - pl.Expr: A pl expression representing the position of the substring within the string.

    Note: If `s` or `sub` is not a pl expression, it will be converted into one.
    """
    s = s if is_polars_expr(s) else create_fix_col(s)
    sub = sub if is_polars_expr(sub) else create_fix_col(sub)
    return s.str(sub)


def pad_left(s: PlStringType, _length: int, pad: str = " ") -> pl.Expr:
    """
    Pad a string on the left side with a specified character to reach a certain length.

    Parameters:
    - s (Any): The string to pad. Can be a pl expression or any other value.
    - length (int): The desired length of the padded string.
    - pad (str): The character to use for padding. Default is " ".

    Returns:
    - pl.Expr: A pl expression representing the padded string.

    Note: If `s` is not a pl expression, it will be converted into one.
    """
    s = s if is_polars_expr(s) else create_fix_col(s)
    return s.str.pad_start(_length, pad)


def pad_right(s: PlStringType, _length: int, pad: str = " ") -> pl.Expr:
    """
    Pad a string on the right side with a specified character to reach a certain length.

    Parameters:
    - s (Any): The string to pad. Can be a pl expression or any other value.
    - length (int): The desired length of the padded string.
    - pad (str): The character to use for padding. Default is " ".

    Returns:
    - pl.Expr: A pl expression representing the padded string.

    Note: If `s` is not a pl expression, it will be converted into one.
    """
    s = s if is_polars_expr(s) else create_fix_col(s)
    return s.str.pad_end(_length, pad)


def trim(s: PlStringType) -> pl.Expr:
    """
    Remove leading and trailing whitespace from a string.

    Parameters:
    - s (Any): The string to trim. Can be a pl expression or any other value.

    Returns:
    - pl.Expr: A pl expression representing the trimmed string.

    Note: If `s` is not a pl expression, it will be converted into one.
    """
    s = s if is_polars_expr(s) else create_fix_col(s)
    return s.str.strip_chars_end().str.strip_chars_start()


def left_trim(s: PlStringType) -> pl.Expr:
    """
    Remove leading whitespace from a string.

    Parameters:
    - s (Any): The string to trim. Can be a pl expression or any other value.

    Returns:
    - pl.Expr: A pl expression representing the trimmed string.

    Note: If `s` is not a pl expression, it will be converted into one.
    """
    s = s if is_polars_expr(s) else create_fix_col(s)
    return s.str.strip_chars_start()


def right_trim(text: PlStringType) -> pl.Expr:
    """
    Remove trailing whitespace from a string.

    Parameters:
    - text: The text to trim. Can be a pl expression or any other value.

    Returns:
    - pl.Expr: A pl expression representing the trimmed string.

    Note: If `s` is not a pl expression, it will be converted into one.
    """
    s = text if is_polars_expr(text) else create_fix_col(text)
    return s.str.strip_chars_end()


def __get_similarity_method(how: str) -> callable:
    match how:
        case 'levenshtein':
            return partial(pds.str_leven, return_sim=True)
        case 'jaro':
            return pds.str_jaro
        case 'jaro_winkler':
            return pds.str_jw
        case 'damerau_levenshtein':
            return partial(pds.str_d_leven, return_sim=True)
        case 'hamming':
            return pds.str_hamming
        case 'fuzzy':
            return pds.str_fuzz
        case 'optimal_string_alignment':
            return pds.str_osa
        case 'sorensen_dice':
            return pds.str_sorensen_dice
        case 'jaccard':
            return pds.str_jaccard
        case _:
            raise ValueError(f"Unknown similarity method: {how}\n\n"
                             f"Possible options are: "
                             f"levenshtein, jaro, jaro_winkler, damerau_levenshtein, "
                             f"hamming, fuzzy, optimal_string_alignment, "
                             f"sorensen_dice, jaccard")


def string_similarity(text: PlStringType, other_text: PlStringType, how: str = 'levenshtein') -> pl.Expr:
    """
    Calculate the similarity between two strings using a specified similarity method.

    Args:
        text (PlStringType): The first string or a Polars expression containing the strings to compare.
        other_text (PlStringType): The second string or a Polars expression containing the strings to compare.
        how (str): The similarity metric to use. Defaults to 'levenshtein'.
                   Possible options are:
                   - 'levenshtein'
                   - 'jaro'
                   - 'jaro_winkler'
                   - 'damerau_levenshtein'
                   - 'hamming'
                   - 'fuzzy'
                   - 'optimal_string_alignment'
                   - 'sorensen_dice'
                   - 'jaccard'

    Returns:
        pl.Expr: A Polars expression that evaluates the similarity between `text` and `other_text`,
                 with a result in the range [0, 1], where 1 means the strings are identical
                 and 0 means no similarity.
    """
    method = partial(__get_similarity_method(how), parallel=True)
    v1 = text if is_polars_expr(text) else pl.lit(text)
    v2 = other_text if is_polars_expr(other_text) else pl.lit(other_text)
    return method(v1, v2)
