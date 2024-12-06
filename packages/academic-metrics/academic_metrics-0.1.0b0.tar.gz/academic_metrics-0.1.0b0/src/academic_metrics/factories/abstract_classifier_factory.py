# abstract_classifier_factory.py
from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from academic_metrics.utils.taxonomy_util import Taxonomy

from academic_metrics.AI.AbstractClassifier import AbstractClassifier
from academic_metrics.configs import (
    configure_logging,
    DEBUG,
)


class ClassifierFactory:
    def __init__(
        self,
        taxonomy: Taxonomy,
        ai_api_key: str,
    ):
        # self.log_file_path: str = os.path.join(
        #     LOG_DIR_PATH, "abstract_classifier_factory.log"
        # )
        # # Set up logger
        # self.logger: logging.Logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.DEBUG)

        # if self.logger.handlers:
        #     self.logger.handlers = []

        # # Add handler if none exists
        # if not self.logger.handlers:
        #     handler: logging.FileHandler = logging.FileHandler(self.log_file_path)
        #     handler.setLevel(logging.DEBUG)
        #     formatter: logging.Formatter = logging.Formatter(
        #         "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        #     )
        #     handler.setFormatter(formatter)
        #     self.logger.addHandler(handler)

        self.logger = configure_logging(
            module_name=__name__,
            log_file_name="abstract_classifier_factory",
            log_level=DEBUG,
        )

        self.logger.info("Initializing ClassifierFactory")

        self.taxonomy: Taxonomy = taxonomy
        self.ai_api_key: str = ai_api_key

        self.logger.info("ClassifierFactory initialized successfully")

    def abstract_classifier_factory(
        self,
        doi_abstract_dict: Dict[str, str],
        extra_context: dict | None = None,
        pre_classification_model: str | None = None,
        classification_model: str | None = None,
        theme_model: str | None = None,
    ) -> AbstractClassifier:
        self.logger.info("Creating AbstractClassifier")
        classifier: AbstractClassifier = AbstractClassifier(
            taxonomy=self.taxonomy,
            doi_to_abstract_dict=doi_abstract_dict,
            api_key=self.ai_api_key,
            extra_context=extra_context,
            pre_classification_model=pre_classification_model,
            classification_model=classification_model,
            theme_model=theme_model,
        )
        self.logger.info("AbstractClassifier created successfully")
        return classifier
