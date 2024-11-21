from __future__ import annotations

from collections import defaultdict

from ..utils.flat_chain import flat_chain
from ..utils.game_options import GameOptions
from ..utils.number_combination_vector import NumberCombinationVector
from ..utils.types import number


__all__ = ["all_results", "verify_feasibility"]


def _divide(a: number, b: number, memo: set[number], integer_only: bool) -> None:
    if b == 0:
        return
    if integer_only:
        div, mod = divmod(a, b)
        if mod == 0:
            memo.add(div)
    else:
        memo.add(a / b)


def _binary_operation(
        a: set[number], b: set[number],
        memo: set[number] | None = None,
        integer_only: bool = True,
) -> set[number]:
    results = set() if memo is None else memo
    for a_val in a:
        for b_val in b:
            results.add(a_val + b_val)
            results.add(a_val - b_val)
            results.add(b_val - a_val)
            results.add(a_val * b_val)
            _divide(a_val, b_val, results, integer_only)
            _divide(b_val, a_val, results, integer_only)
    return results


def all_results(numbers: list[number], options: GameOptions) -> set[number]:
    total_count = len(numbers)
    if total_count == 0:
        return set()
    elif total_count == 1:
        return set(numbers)

    empty_vector = NumberCombinationVector.init(numbers)
    total_vector = empty_vector.add_numbers(numbers)
    memo: dict[number, dict[NumberCombinationVector, set[number]]] = defaultdict(lambda: defaultdict(set))
    memo[1] = {
        empty_vector.add_number(number): {number}
        for number in numbers
    }

    for curr_count in range(1, total_count):
        focused_memo = memo[curr_count]
        other_itemss = [
            memo[i].items()
            for i in range(min(curr_count, total_count - curr_count), 0, -1)
        ]

        for focused_combination, focused_results in focused_memo.items():
            for other_combination, other_results in flat_chain(other_itemss):
                combined_combination = focused_combination + other_combination
                if not (combined_combination <= total_vector):
                    continue
                combined_total_count = combined_combination.total_count()
                _binary_operation(
                    focused_results,
                    other_results,
                    memo[combined_total_count][combined_combination],
                    options.integer_only,
                )

    if options.must_use_all:
        return set(flat_chain(memo[total_count].values()))
    else:
        return set(
            result
            for memo_i in memo.values()
            for results in memo_i.values()
            for result in results
        )


def verify_feasibility(
        numbers: list[number], target: number,
        options: GameOptions,
) -> bool:
    total_count = len(numbers)
    if total_count == 0:
        return False
    elif total_count == 1:
        return numbers[0] == target

    if not options.must_use_all and target in numbers:
        return True

    empty_vector = NumberCombinationVector.init(numbers)
    total_vector = empty_vector.add_numbers(numbers)
    memo: dict[number, dict[NumberCombinationVector, set[number]]] = defaultdict(lambda: defaultdict(set))
    memo[1] = {
        empty_vector.add_number(number): {number}
        for number in numbers
    }

    for curr_count in range(1, total_count):
        focused_memo = memo[curr_count]
        other_itemss = [
            memo[i].items()
            for i in range(min(curr_count, total_count - curr_count), 0, -1)
        ]

        for focused_combination, focused_results in focused_memo.items():
            for other_combination, other_results in flat_chain(other_itemss):
                combined_combination = focused_combination + other_combination
                if not (combined_combination <= total_vector):
                    continue
                combined_total_count = combined_combination.total_count()
                combined_results = memo[combined_total_count][combined_combination]
                _binary_operation(focused_results, other_results, combined_results, options.integer_only)
                if (
                        (not options.must_use_all or combined_total_count == total_count)
                        and target in combined_results
                ):
                    return True

    if not options.integer_only:
        return any(
            abs(result - target) < 1e-6
            for result in flat_chain(memo[total_count].values())
        )
    return False


if __name__ == "__main__":
    default_options = GameOptions()
    float_allowed_options = GameOptions(integer_only=False)
    assert verify_feasibility([2, 10, 2, 2], 24, default_options)
    assert verify_feasibility([1, 4, 7, 9], 24, default_options)
    assert not verify_feasibility([11, 11, 11, 11], 24, default_options)
    assert not verify_feasibility([1, 3, 4, 6], 24, default_options)
    assert verify_feasibility([1, 3, 4, 6], 24, float_allowed_options)
    assert not verify_feasibility([1, 7, 13, 37], 1, default_options)
    assert verify_feasibility([1, 7, 13, 37], 1, GameOptions(must_use_all=False))
    # print(sorted(list(_all_results([1, 3, 4, 6], default_options))))
    