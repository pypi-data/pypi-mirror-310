import logging
import os
from pathlib import Path
from typing import Generator, Optional

import pandas as pd

from ..attack_provider.attack_registry import register_test
from ..attack_provider.test_base import StatusUpdate, TestBase
from ..client.attack_config import AttackConfig
from ..client.chat_client import ChatSession
from ..client.client_config import ClientConfig
from .utils import evaluate_response

logger = logging.getLogger(__name__)


@register_test
class TestHarmfulBehaviors(TestBase):
    """Challenges the LLM with a dataset of harmful behavior prompts."""

    test_name = "harmful_behavior"

    def __init__(
        self,
        client_config: ClientConfig,
        attack_config: AttackConfig,
        artifacts_path: Optional[str] = None,
        num_attempts: int = 0,
    ):
        super().__init__(client_config, attack_config, artifacts_path=artifacts_path, num_attempts=num_attempts)

    def _prepare_attack_data(self, attack_prompts: list[str], responses: list[str], statuses: list[str]) -> None:
        """
        Prepares attack data in a structured DataFrame format and saves it as a CSV file.

        Args:
            attack_prompts (list[str]): List of attack texts generated during the test.
            responses (list[str]): List of responses from the target system.
            statuses (list[str]): List of statuses ('broken', 'resilient', 'error') corresponding to each attack.

        Returns:
            None
        """
        # Create a DataFrame from the lists
        df = pd.DataFrame({"attack_text": attack_prompts, "response_text": responses, "status": statuses})

        # Save the DataFrame as a CSV file to the artifacts path
        if self.artifacts_path:
            csv_path = os.path.join(self.artifacts_path, f"{self.test_name}.csv")
            df.to_csv(csv_path, index=False)
            logging.info(f"Harmful Behavior attack report saved to {csv_path}")

    def run(self) -> Generator[StatusUpdate, None, None]:
        attack_prompts = []
        responses = []
        statuses = []
        # Getting the path to the directory where the file is located harmful_behavior.py
        current_dir = Path(__file__).parent
        dataset_filename = current_dir.parent / "attack_data" / "harmful_behavior.parquet"

        logger.info(f"Dataset filename: {dataset_filename}")
        data = pd.read_parquet(dataset_filename, engine="fastparquet")
        rows_count = data.shape[0]

        if rows_count > self.num_attempts:
            # If dataset is larger than requested number of samples, reduce dataset by taking num_attempts samples
            data = data.sample(
                n=self.num_attempts, random_state=42
            )  # constant `random_state` for better reproducibility

        # Generate list of attack prompt variations
        yield StatusUpdate(
            self.client_config,
            self.test_name,
            self.status,
            "Generating",
            0,
            self.num_attempts
        )

        for attack_prompt_index, row in data.iterrows():
            attack_prompt = row["goal"]
            attack_prompts.append(attack_prompt)
            target = row["target"]
            logger.info(f"Test '{self.test_name}': generated attack prompt #{attack_prompt_index}: {attack_prompt}")
            yield StatusUpdate(
                self.client_config,
                self.test_name,
                self.status,
                "Generating",
                attack_prompt_index,
                self.num_attempts,
            )

            chat = ChatSession(
                self.client_config.get_target_client(),
                self.client_config.get_system_prompts(),
            )
            response = chat.say(attack_prompt)
            if not response:
                logger.warning("Error while attacking against target LLM (didn't receive response) ...")
                self.status.report_error(attack_prompt)
                current_status = "Error"
            else:
                # Verify if the response is compliant
                verified = evaluate_response(
                    self.attack_config.attack_client.get_target_client(), response, row["target"]
                )
                logger.info(f"Test '{self.test_name}': attack prompt #{attack_prompt_index}: {attack_prompt}")
                logger.info(f"Test '{self.test_name}': expected response #{attack_prompt_index}: {target}")
                logger.info(
                    f"Test '{self.test_name}': attack response #{attack_prompt_index} break_success={verified}): {response}"
                )

                if verified:
                    self.status.report_breach(attack_prompt, response)
                    current_status = "Broken"
                else:
                    self.status.report_resilient(attack_prompt, response)
                    current_status = "Resilient"

            # Append data for report
            responses.append(response)
            statuses.append(current_status)

            yield StatusUpdate(
                self.client_config,
                self.test_name,
                self.status,
                "Attacking",
                attack_prompt_index,
                self.num_attempts,
            )

        # Prepare data for report generation
        self._prepare_attack_data(attack_prompts, responses, statuses)

        yield StatusUpdate(
            self.client_config,
            self.test_name,
            self.status,
            "Completed",
            self.num_attempts,
            self.num_attempts,
        )
