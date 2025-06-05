# agents/simple_verifier_agent.py

from .base_agent import BaseVerificationAgent # Relative import

class SimpleVerifierAgent(BaseVerificationAgent):
    """
    A very simple MVP1 verification agent.
    It checks if a 'content_hash' exists and has a certain minimum length.
    It does not look at actual content for MVP1.
    """
    MIN_HASH_LENGTH = 10 # Arbitrary minimum length for a hash to be "plausible"

    def __init__(self, agent_id="simple_verifier_v1", agent_version="0.1.0"):
        # This agent can attempt to verify any content type as it only looks at metadata.
        super().__init__(agent_id, agent_version, supported_content_types=None) 

    def verify_claim_data(self, claim_data, claim_content=None):
        """
        Verifies the claim based on the presence and length of 'content_hash'.
        """
        print(f"Agent '{self.agent_id}' processing claim_id: {claim_data.get('claim_id')}")

        content_hash = claim_data.get("content_hash")
        
        if not content_hash:
            details = "Claim is missing 'content_hash' in its data."
            print(f"Verification failed: {details}")
            return self.generate_verification_event(
                verdict="unverified", 
                details=details,
                confidence_score=0.1 # Low confidence due to missing crucial data
            )

        if isinstance(content_hash, str) and len(content_hash) >= self.MIN_HASH_LENGTH:
            details = f"Content hash found with sufficient length ({len(content_hash)} >= {self.MIN_HASH_LENGTH})."
            print(f"Verification preliminary pass: {details}")
            return self.generate_verification_event(
                verdict="verified_preliminary", # Custom status for MVP
                details=details,
                confidence_score=0.6 # Moderate confidence for this simple check
            )
        else:
            details = f"Content hash is too short or not a string. Length: {len(content_hash) if isinstance(content_hash, str) else 'N/A'}. Min required: {self.MIN_HASH_LENGTH}."
            print(f"Verification failed: {details}")
            return self.generate_verification_event(
                verdict="unverified",
                details=details,
                confidence_score=0.2
            )

if __name__ == '__main__':
    # Test the SimpleVerifierAgent
    agent = SimpleVerifierAgent()
    print(f"\n--- Testing Agent: {agent.get_info()['agent_id']} ---")

    test_claim_valid = {
        "claim_id": "test_valid_001",
        "content_hash": "abcdef1234567890uvwxyz", # Valid length
        "content_type": "text/plain"
    }
    result_valid = agent.verify_claim_data(test_claim_valid)
    print("Verification Result (Valid Claim):")
    import json
    print(json.dumps(result_valid, indent=2))

    test_claim_short_hash = {
        "claim_id": "test_short_002",
        "content_hash": "abc", # Too short
        "content_type": "image/jpeg"
    }
    result_short_hash = agent.verify_claim_data(test_claim_short_hash)
    print("\nVerification Result (Short Hash Claim):")
    print(json.dumps(result_short_hash, indent=2))

    test_claim_no_hash = {
        "claim_id": "test_no_hash_003",
        # "content_hash": missing
        "content_type": "application/json"
    }
    result_no_hash = agent.verify_claim_data(test_claim_no_hash)
    print("\nVerification Result (No Hash Claim):")
    print(json.dumps(result_no_hash, indent=2))

    print(f"\nAgent Info: {json.dumps(agent.get_info(), indent=2)}")
    print(f"Can agent verify 'text/plain'? {agent.can_verify('text/plain')}")
    print(f"Can agent verify 'video/mp4'? {agent.can_verify('video/mp4')}")