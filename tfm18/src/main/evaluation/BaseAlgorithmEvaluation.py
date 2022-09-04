from abc import abstractmethod

from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType


class BaseAlgorithmEvaluation:

    @abstractmethod
    def get_type(self) -> AlgorithmEvaluationType:
        pass

    def evaluate(self, expected: list[float], result: list[float]) -> float:
        len_expected = len(expected)
        len_result = len(result)
        if len_expected != len_result:
            raise Exception("Both list should have the same value! %d!=%d" % (len_expected, len_result))
        return self._evaluate(expected=expected, result=result)

    @abstractmethod
    def _evaluate(self, expected: list[float], result: list[float]) -> float:
        pass
