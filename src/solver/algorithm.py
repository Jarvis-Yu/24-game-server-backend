from __future__ import annotations

from collections import defaultdict

from ..utils.expression import BiOpExpression, Expression, NumberExpression
from ..utils.flat_chain import flat_chain
from ..utils.game_options import GameOptions
from ..utils.number_combination_vector import NumberCombinationVector
from ..utils.types import number


__all__ = ["all_results", "find_solution_for_target"]


def _divide(
        a_val: number, b_val: number, a_exp: Expression, b_exp: Expression,
        memo: dict[number, Expression], integer_only: bool
) -> None:
    if b_val == 0:
        return
    if integer_only:
        div, mod = divmod(a_val, b_val)
        if mod == 0:
            memo[div] = BiOpExpression.div(a_exp, b_exp)
    else:
        memo[a_val / b_val] = BiOpExpression.div(a_exp, b_exp)


def _binary_operation(
        a: dict[number, Expression], b: dict[number, Expression],
        memo: dict[number, Expression] | None = None,
        integer_only: bool = True,
) -> dict[number, Expression]:
    results = dict() if memo is None else memo
    for a_val, a_exp in a.items():
        for b_val, b_exp in b.items():
            results[a_val + b_val] = BiOpExpression.add(a_exp, b_exp)
            results[a_val - b_val] = BiOpExpression.sub(a_exp, b_exp)
            results[b_val - a_val] = BiOpExpression.sub(b_exp, a_exp)
            results[a_val * b_val] = BiOpExpression.mul(a_exp, b_exp)
            _divide(a_val, b_val, a_exp, b_exp, results, integer_only)
            _divide(b_val, a_val, b_exp, a_exp, results, integer_only)
    return results


def all_results(numbers: list[number], options: GameOptions) -> dict[number, Expression]:
    total_count = len(numbers)
    if total_count == 0:
        return dict()
    elif total_count == 1:
        return {
            number: NumberExpression(number)
            for number in numbers
        }

    empty_vector = NumberCombinationVector.init(numbers)
    total_vector = empty_vector.add_numbers(numbers)
    memo: dict[int, dict[NumberCombinationVector, dict[number, Expression]]] = defaultdict(lambda: defaultdict(dict))
    memo[1] = {
        empty_vector.add_number(number): {number: NumberExpression(number)}
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

    if options.must_use_all:
        return {
            result: expression
            for comb_result_dict in memo[total_count].values()
            for result, expression in comb_result_dict.items()
        }
    else:
        return {
            result: expression
            for memo_i in memo.values()
            for comb_result_dict in memo_i.values()
            for result, expression in comb_result_dict.items()
        }


def find_solution_for_target(
        numbers: list[number], target: number,
        options: GameOptions,
) -> Expression | None:
    total_count = len(numbers)
    if total_count == 0:
        return False
    elif total_count == 1:
        return numbers[0] == target

    if not options.must_use_all and target in numbers:
        return True

    empty_vector = NumberCombinationVector.init(numbers)
    total_vector = empty_vector.add_numbers(numbers)
    memo: dict[int, dict[NumberCombinationVector, dict[number, Expression]]] = defaultdict(lambda: defaultdict(dict))
    memo[1] = {
        empty_vector.add_number(number): {number: NumberExpression(number)}
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
                    return combined_results[target]

    if not options.integer_only:
        for comb_result_dict in memo[total_count].values():
            for result, expression in comb_result_dict.items():
                if abs(result - target) < 1e-6:
                    return expression
    return None


if __name__ == "__main__":
    default_options = GameOptions()
    float_allowed_options = GameOptions(integer_only=False)
    assert find_solution_for_target([2, 10, 2, 2], 24, default_options) is not None
    assert find_solution_for_target([1, 4, 7, 9], 24, default_options) is not None
    assert find_solution_for_target([11, 11, 11, 11], 24, default_options) is None
    assert find_solution_for_target([1, 3, 4, 6], 24, default_options) is None
    assert find_solution_for_target([1, 3, 4, 6], 24, float_allowed_options) is not None
    assert find_solution_for_target([1, 7, 13, 37], 1, default_options) is None
    assert find_solution_for_target([1, 7, 13, 37], 1, GameOptions(must_use_all=False)) is not None

    # results = all_results([3, 3, 8, 8], default_options)
    # for result in sorted(list(results.keys())):
    #     print(f"{result}: {results[result]}")
    