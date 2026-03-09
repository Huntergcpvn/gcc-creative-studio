# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os

import firebase_admin
from firebase_admin import credentials

logger = logging.getLogger(__name__)


class FirebaseClient:
    """
    A class to initialize the Firebase Admin SDK and provide access to Firestore and Auth.
    """

    def __init__(self):
        """
        Initializes the Firebase Admin SDK with credentials.
        """
        try:
            # Init Firebase Creds
            if not firebase_admin._apps:  # Check if already initialized
                cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

                if cred_path:
                    logger.info(
                        f"Initializing Firebase Admin SDK with credentials from: {cred_path}"
                    )
                    if not os.path.exists(cred_path):
                        raise FileNotFoundError(
                            f"Firebase credentials file specified but not found at {cred_path}"
                        )
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred)
                else:
                    # If FIREBASE_CREDENTIALS_PATH is not set,
                    # try to initialize with Application Default Credentials (ADC).
                    logger.info("Initializing Firebase Admin SDK using ADC.")
                    firebase_admin.initialize_app()

                logger.info(
                    f"Firebase App Name: {firebase_admin.get_app().name}"
                )

        except Exception as e:
            logger.critical(
                f"CRITICAL: Error initializing Firebase Admin SDK: {e}",
                exc_info=True,
            )
            raise RuntimeError(f"Failed to initialize Firebase Admin SDK: {e}")


# Initialize the client. On Cloud Run, ADC will be used automatically.
firebase_client = FirebaseClient()
