import datetime
import statistics
from typing import Tuple, Optional, Any

import sklearn
from pandas import DataFrame
from sklearn.metrics import make_scorer

from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.execution.TripExecutorConfigDto import TripExecutorConfigDto
from tfm18.src.main.ml.PredictorLearnerConfig import PredictorLearnerConfig


class PredictorLearner:
    config: PredictorLearnerConfig
    trip_executor: TripExecutor

    def __init__(self, config: PredictorLearnerConfig):
        self.config = config
        self.trip_executor = TripExecutor()

    def train_full_trip_list(self):
        # Start recording pre-training time
        pre_train_time_start_time: datetime = datetime.datetime.now()

        input_list_of_lists: list[list[float]]
        output_list_of_lists: list[list[float]]
        input_list_of_lists, output_list_of_lists = self.get_input_output_list_of_lists(
            dataset_trip_dto_list=self.config.training_dataset_trip_list
        )
        input_column_name_list: list[str] = [
            'FBD', 'FBE', 'AEC', 'timestamp [min]', 'soc [%]', 'iec_power [kWh/100km]', 'current [A]', 'speed [km/h]',
            'power [kW]', 'ac_power [kW]', 'distance [km]'
        ]
        input_dataframe: DataFrame = DataFrame(input_list_of_lists, columns=input_column_name_list)
        output_column_name_list: list[str] = ['expected eRange [km]']
        output_dataframe: DataFrame = DataFrame(output_list_of_lists, columns=output_column_name_list)

        # The cross validation uses the full dataset
        cv_input_list_of_lists: list[list[float]]
        cv_output_list_of_lists: list[list[float]]
        cv_input_list_of_lists, cv_output_list_of_lists = self.get_input_output_list_of_lists(
            dataset_trip_dto_list=[self.config.run_dataset_trip_dto]
        )
        cv_input_list_of_lists.extend(input_list_of_lists)
        cv_output_list_of_lists.extend(output_list_of_lists)
        cv_input_dataframe: DataFrame = DataFrame(cv_input_list_of_lists, columns=input_column_name_list)
        cv_output_dataframe: DataFrame = DataFrame(cv_output_list_of_lists, columns=output_column_name_list)

        pre_train_time_delta_secs: float = (datetime.datetime.now() - pre_train_time_start_time).total_seconds()
        print("Time for pre training: %.2f" % pre_train_time_delta_secs)

        train_time_start_time: datetime = datetime.datetime.now()
        for algorithm in self.config.algorithms_to_train:
            algorithm_time_start_time: datetime = datetime.datetime.now()
            algorithm.learn_from_dataframes(input_dataframe=input_dataframe, expected_output_dataframe=output_dataframe)
            algorithm_time_delta_secs: float = (datetime.datetime.now() - algorithm_time_start_time).total_seconds()
            print(
                "Time for %s algorithm training: %.2f" %
                (algorithm.get_algorithm_type().value[0], algorithm_time_delta_secs)
            )
        train_time_delta_secs: float = (datetime.datetime.now() - train_time_start_time).total_seconds()
        print("Time for training: %.2f" % train_time_delta_secs)

        self.cross_validation(
            cv_input_dataframe=cv_input_dataframe,
            cv_output_dataframe=cv_output_dataframe,
            variable_count=len(input_column_name_list)
        )

    def get_input_output_list_of_lists(
        self,
        dataset_trip_dto_list: list[DatasetTripDto]
    ) -> Tuple[list[list], list[list]]:
        input_list_of_lists = []
        output_list_of_lists = []
        for dataset_trip_dto in dataset_trip_dto_list:

            expected_output_list: list[float] = self.trip_executor.execute_trip(
                config=TripExecutorConfigDto(
                    dataset_trip_dto=dataset_trip_dto,
                    enabled_algorithm_types=[self.config.expected_algorithm_type],
                    print_execution_time=False
                )
            ).eRange_distance_results[self.config.expected_algorithm_type]
            for expected_output in expected_output_list:
                output_list_of_lists.append([expected_output])
            # output_list_of_lists.append(expected_output_list)
            for timestamp in dataset_trip_dto.dataset_timestamp_dto_list:
                input_list_of_lists.append(
                    [
                        dataset_trip_dto.vehicle_static_data.FBD_km,
                        dataset_trip_dto.vehicle_static_data.FBE_kWh,
                        dataset_trip_dto.vehicle_static_data.AEC_KWh_km,
                        timestamp.timestamp_min,
                        timestamp.soc_percentage,
                        timestamp.iec_power_KWh_by_100km,
                        timestamp.current_ampers,
                        timestamp.speed_kmh,
                        timestamp.power_kW,
                        timestamp.ac_power_kW,
                        timestamp.distance_kM
                    ]
                )

        return input_list_of_lists, output_list_of_lists

    def cross_validation(self, cv_input_dataframe: DataFrame, cv_output_dataframe: DataFrame, variable_count: int):
        cv_start_time: datetime = datetime.datetime.now()
        for ml_algorithm in self.config.algorithms_to_train:
            cv_scoring_dict: dict[str, Any] = dict()
            evaluation: BaseAlgorithmEvaluation
            for evaluation in self.config.evaluation_algorithms:
                evaluation_type: AlgorithmEvaluationType = evaluation.get_type()
                scikit_learn_evaluation_name: Optional[str] = evaluation_type.value[2]
                evaluation_name: str = evaluation_type.value[0]
                # Use Scikit-learn's algorithm name
                if scikit_learn_evaluation_name is not None:
                    cv_scoring_dict[evaluation_name] = scikit_learn_evaluation_name
                # Use custom evaluation algorithm as Scikit-learn does not have its algorithm name
                else:
                    def scorer(y_expected_dataframe: DataFrame, y_predicted_dataframe: DataFrame):
                        # The dataframe contains an array of arrays with one value each
                        # and must be turned to 1 dimensional array
                        return evaluation.evaluate(
                            expected=y_expected_dataframe.ravel().tolist(),
                            result=y_predicted_dataframe.ravel().tolist(),
                            variable_count=variable_count
                        )

                    cv_scoring_dict[evaluation_name] = make_scorer(
                        score_func=scorer,
                        greater_is_better=evaluation_type.value[3]
                    )

            cv_ml_algo_start_time: datetime = datetime.datetime.now()
            k_fold_k: int = 20
            cv_scores_dict: dict[str, list[float]] = sklearn.model_selection.cross_validate(
                estimator=ml_algorithm.get_model(),
                X=cv_input_dataframe.values,
                y=cv_output_dataframe.values,
                scoring=cv_scoring_dict,
                cv=sklearn.model_selection.KFold(
                    n_splits=k_fold_k
                ),
                return_train_score=True,
                n_jobs=-1
                # n_jobs=None # Disabled parallel execution
            )
            cv_ml_algo_time_delta_secs: float = (datetime.datetime.now() - cv_ml_algo_start_time).total_seconds()
            print(
                "Time for %s cross validation: %.2f" %
                (ml_algorithm.get_algorithm_type().value[0], cv_ml_algo_time_delta_secs)
            )

            evaluation_type: AlgorithmEvaluationType
            for evaluation_type in self.config.algorithm_evaluation_types:
                evaluation_type_name: str = evaluation_type.value[0]
                evaluation_result: float = statistics.mean(cv_scores_dict["test_%s" % evaluation_type_name])
                scikit_learn_evaluation_name: Optional[str] = evaluation_type.value[2]

                # Fix higher is worse algorithms that are negated on scikit-learn
                if scikit_learn_evaluation_name is not None and scikit_learn_evaluation_name.startswith("neg_"):
                    evaluation_result = -evaluation_result

                print(
                    "K=%d Fold cross validation %s performance of %s algorithm: %.3f" % (
                        k_fold_k,
                        evaluation_type_name,
                        ml_algorithm.get_algorithm_type().value[0],
                        evaluation_result
                    )
                )
        cv_time_delta_secs: float = (datetime.datetime.now() - cv_start_time).total_seconds()
        print("Time for all ML algorithms cross validation: %.2f" % cv_time_delta_secs)
