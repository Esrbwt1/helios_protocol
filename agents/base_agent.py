# agents/base_agent.py

from abc import ABC, abstractmethod
import datetime

class BaseVerificationAgent(ABC):
    def __init__(self, agent_id, agent_version, supported_content_types=None):
        self.agent_id = agent_id
        self.agent_version = agent_version
        # List of content types this agent can process, e.g., ["text/plain", "image/jpeg"]
        # If None, it's assumed it can attempt to process any type (with potential failure).
        self.supported_content_types = supported_content_types if supported_content_types else []

    @abstractmethod
    def verify_claim_data(self, claim_data, claim_content=None):
        """
        The core verification logic for the agent.
        This method must be implemented by all subclasses.

        Args:
            claim_data (dict): The metadata and information about the claim.
            claim_content (bytes, optional): The actual content being verified. 
                                             May not always be available or needed by every agent.

        Returns:
            dict: A verification result dictionary containing at least:
                  - "agent_id": self.agent_id
                  - "agent_version": self.agent_version
                  - "timestamp": UTC ISO format string
                  - "verdict": "verified", "unverified", "error", "unable_to_verify"
                  - "confidence_score": float (0.0 to 1.0), if applicable
                  - "details": dict or str, providing more information or evidence.
        """
        pass

    def generate_verification_event(self, verdict, details, confidence_score=None):
        """
        Helper method to create a standardized verification event structure.
        """
        event = {
            "agent_id": self.agent_id,
            "agent_version": self.agent_version,
            "timestamp": str(datetime.datetime.utcnow().isoformat()),
            "verdict": verdict, # e.g., "verified", "unverified", "error"
            "details": details # Specific findings or evidence
        }
        if confidence_score is not None:
            event["confidence_score"] = confidence_score
        return event

    def can_verify(self, content_type):
        """
        Checks if this agent supports the given content type.
        If self.supported_content_types is empty, it's assumed to try anything.
        """
        if not self.supported_content_types:
            return True # Can attempt any
        return content_type in self.supported_content_types

    def get_info(self):
        """
        Returns information about the agent.
        """
        return {
            "agent_id": self.agent_id,
            "agent_version": self.agent_version,
            "supported_content_types": self.supported_content_types,
            "description": self.__doc__ if self.__doc__ else "No description provided."
        }

if __name__ == '__main__':
    # This class is abstract and cannot be instantiated directly.
    # To test, you'd need a concrete subclass.
    print("BaseVerificationAgent is an abstract class and cannot be run directly.")
    print("It defines the interface for all verification agents.")