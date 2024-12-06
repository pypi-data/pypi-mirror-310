import glob
import json
import os
import pathlib
import pickle
from typing import Dict, Optional

from giotto_llm.type_aliases import JSONTask


class ReaderMany:
    """Read ARC challenge data from JSON with many tasks."""

    def __init__(
        self,
        dataset_dir: str,
        dataset_type: str,
        read_test_output: bool = True,
        subset_task_ids: Optional[list[str]] = None,
    ) -> None:
        self.dataset_dir = dataset_dir
        self.dataset_type = dataset_type
        self.read_test_output = read_test_output
        self.subset_task_ids = subset_task_ids

    def read_tasks(self) -> Dict[str, Dict]:
        """Read all tasks and put test input/output grids in the same dict."""
        tasks_challenges = self.read_challenges()
        if self.read_test_output:
            tasks_solutions = self.read_solutions()
            task_ids = sorted(tasks_challenges.keys())
            tasks = dict()
            for task_id in task_ids:
                if self.subset_task_ids is None or task_id in self.subset_task_ids:
                    tmp_train = tasks_challenges[task_id]["train"]
                    tmp_test_in = [el["input"] for el in tasks_challenges[task_id]["test"]]
                    tmp_test_out = tasks_solutions[task_id]
                    assert len(tmp_test_in) == len(tmp_test_out)

                    tasks[task_id] = {
                        "train": tmp_train,
                        "test": [
                            {"input": tmp_test_in[idx], "output": tmp_test_out[idx]}
                            for idx in range(len(tmp_test_in))
                        ],
                    }

            return tasks
        else:
            return tasks_challenges

    def read_challenges(self) -> Dict:
        path_to_challenges: str = os.path.join(
            self.dataset_dir, f"arc-agi_{self.dataset_type}_challenges.json"
        )
        with open(path_to_challenges, "rb") as f:
            tasks_challenges: dict = json.load(f)
        return tasks_challenges

    def read_solutions(self) -> Dict:
        path_to_solutions = os.path.join(
            self.dataset_dir, f"arc-agi_{self.dataset_type}_solutions.json"
        )
        with open(path_to_solutions, "rb") as f:
            tasks_solutions: dict = json.load(f)

        return tasks_solutions


class ReaderOneByOne:
    """Read ARC challenge data one JSON file at a time."""

    def __init__(
        self,
        dataset_dir: str,
        read_test_output: bool = True,
    ) -> None:
        self.dataset_dir = str(pathlib.Path(dataset_dir).absolute())
        self.read_test_output = read_test_output

    def read_tasks(self) -> Dict[str, Dict]:
        """Read all tasks in self.dataset_dir"""
        tasks = dict()

        paths = sorted(glob.glob(self.dataset_dir + "/*.json"))
        for path_to_json_file in paths:
            task_id = path_to_json_file.split("/")[-1].split(".")[0]
            with open(path_to_json_file, "rb") as f:
                tmp_task = json.load(f)
            if not self.read_test_output:
                # Note: dropping output grids in test pairs
                for idx_i in range(len(tmp_task["test"])):
                    del tmp_task["test"][idx_i]["output"]

            tasks[task_id] = tmp_task
        return tasks


class ReaderPickle:
    """Read ARC challenge data from Pickle file."""

    def __init__(
        self,
        dataset_dir: str,
        dataset_category: str,
        read_test_output: bool = True,
    ) -> None:
        self.dataset_dir = str(pathlib.Path(dataset_dir).absolute())
        self.dataset_category = dataset_category
        self.read_test_output = read_test_output

    def read_tasks(self) -> Dict[str, Dict]:
        """Read all tasks in self.dataset_dir of self.dataset_category."""
        tasks: dict = dict()

        path_to_pickle_file = os.path.join(self.dataset_dir, f"{self.dataset_category}.pickle")
        tasks = dict()
        with open(path_to_pickle_file, "rb") as file_handle:
            tmp_tasks = pickle.load(file_handle)

            if not self.read_test_output:
                # Note: dropping output grids in test pairs
                for task_id in tmp_tasks.keys():
                    for idx_i in range(len(tmp_tasks[task_id]["test"])):
                        del tmp_tasks[task_id]["test"][idx_i]["output"]

            tasks.update(tmp_tasks)

        return tasks


class ReaderManyOnlineFinetuning:
    """Read ARC challenge data from JSON with many tasks for online-fine-tuning."""

    def __init__(
        self,
        dataset_dir: str,
        dataset_type: str,
        is_test: bool = False,
        subset_task_ids: Optional[list[str]] = None,
    ) -> None:
        self.dataset_dir = dataset_dir
        self.dataset_type = dataset_type
        self.is_test = is_test
        self.subset_task_ids = subset_task_ids

    def read_tasks(self) -> Dict[str, Dict]:
        """Read all tasks and put test input/output grids in the same dict."""
        tasks_challenges = self.read_challenges()
        tasks_solutions = self.read_solutions()
        task_ids = sorted(
            tasks_challenges.keys() if self.subset_task_ids is None else self.subset_task_ids
        )
        tasks = dict()
        for task_id in task_ids:
            tmp_train = tasks_challenges[task_id]["train"]
            if not self.is_test:
                for idx in range(len(tmp_train)):
                    # use the all train grids as train input and idx as test
                    cur_train = tmp_train.copy()
                    cur_test = cur_train.pop(idx)
                    tasks[f"{task_id}_{idx}"] = {
                        "train": cur_train,
                        "test": [{"input": cur_test["input"], "output": cur_test["output"]}],
                    }
            else:
                tmp_test_in = [el["input"] for el in tasks_challenges[task_id]["test"]]
                tmp_test_out = tasks_solutions[task_id]
                assert len(tmp_test_in) == len(tmp_test_out)
                tasks[task_id] = {
                    "train": tmp_train,
                    "test": [
                        {"input": tmp_test_in[idx], "output": tmp_test_out[idx]}
                        for idx in range(len(tmp_test_in))
                    ],
                }

        return tasks

    def read_challenges(self) -> Dict:
        path_to_challenges: str = os.path.join(
            self.dataset_dir, f"arc-agi_{self.dataset_type}_challenges.json"
        )
        with open(path_to_challenges, "rb") as f:
            tasks_challenges: dict = json.load(f)

        return tasks_challenges

    def read_solutions(self) -> Dict:
        path_to_solutions = os.path.join(
            self.dataset_dir, f"arc-agi_{self.dataset_type}_solutions.json"
        )
        with open(path_to_solutions, "rb") as f:
            tasks_solutions: dict = json.load(f)

        return tasks_solutions


class ReaderOneOnlineFinetuning:
    """Read ARC challenge data from JSON with many tasks for online-fine-tuning."""

    def __init__(  # type: ignore
        self,
        task_name,
        demo_tasks,
        test_solutions=None,
        is_test: bool = False,
    ) -> None:
        self.task_name = task_name
        self.demo_tasks = demo_tasks
        self.test_solutions = test_solutions
        self.is_test = is_test

    def read_tasks(self) -> Dict[str, Dict]:
        tmp_train = self.demo_tasks["train"]
        tasks = {}
        if not self.is_test:
            for idx in range(len(tmp_train)):
                # use the all train grids as train input and idx as test
                cur_train = tmp_train.copy()
                cur_test = cur_train.pop(idx)
                tasks[f"{self.task_name}_{idx}"] = {
                    "train": cur_train,
                    "test": [{"input": cur_test["input"], "output": cur_test["output"]}],
                }
        else:
            tmp_test_in = [el["input"] for el in self.demo_tasks["test"]]
            assert len(tmp_test_in) == len(self.test_solutions)
            tasks[self.task_name] = {
                "train": tmp_train,
                "test": [
                    {"input": tmp_test_in[idx], "output": self.test_solutions[idx]}
                    for idx in range(len(tmp_test_in))
                ],
            }
        return tasks
