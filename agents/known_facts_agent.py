# agents/known_facts_agent.py

from .base_agent import BaseVerificationAgent # Relative import
import datetime

class KnownFactsAgent(BaseVerificationAgent):
    """
    An agent that "verifies" claims against a predefined set of "known facts"
    or rules related to the claim's metadata.
    For MVP1, this is a very simplistic rule-based check.
    """

    # Example "known facts":
    # A real system might load these from a config file or a database.
    KNOWN_SUBMITTERS = {
        "official_press_agency_001": {"reputation": 0.9, "category": "news_outlet"},
        "research_institute_alpha": {"reputation": 0.85, "category": "science"},
        "known_disinfo_source_xyz": {"reputation": 0.1, "category": "disinformation_actor"}
    }
    
    # Example rules based on content_type or metadata fields
    RULES_FOR_CONTENT_TYPE = {
        "application/pdf": {
            "metadata_must_contain": ["author", "creation_date"],
            "author_must_not_be": ["anonymous_unverified"]
        },
        "image/jpeg": {
            "metadata_should_contain": ["camera_model", "gps_location"],
            "metadata_flag_if_missing_all": ["camera_model", "gps_location", "creation_software"]
        }
    }

    def __init__(self, agent_id="known_facts_v1", agent_version="0.1.0"):
        super().__init__(agent_id, agent_version, supported_content_types=None) # Can attempt any

    def verify_claim_data(self, claim_data, claim_content=None):
        print(f"Agent '{self.agent_id}' processing claim_id: {claim_data.get('claim_id')}")
        
        verdicts = []
        details_log = []
        confidence_scores = []

        submitter_id = claim_data.get("submitter_id")
        content_type = claim_data.get("content_type")
        metadata = claim_data.get("metadata", {})

        # 1. Check submitter reputation
        if submitter_id in self.KNOWN_SUBMITTERS:
            submitter_info = self.KNOWN_SUBMITTERS[submitter_id]
            details_log.append(f"Submitter '{submitter_id}' found in known list. Reputation: {submitter_info['reputation']}.")
            confidence_scores.append(submitter_info['reputation'])
            if submitter_info["reputation"] < 0.3: # Arbitrary threshold
                verdicts.append("suspicious_source")
        else:
            details_log.append(f"Submitter '{submitter_id}' not in known list. Considered neutral/unknown for this check.")
            confidence_scores.append(0.5) # Neutral confidence for unknown submitter

        # 2. Check rules for content_type
        if content_type in self.RULES_FOR_CONTENT_TYPE:
            rules = self.RULES_FOR_CONTENT_TYPE[content_type]
            
            # Check for mandatory metadata
            if "metadata_must_contain" in rules:
                missing_mandatory = [key for key in rules["metadata_must_contain"] if key not in metadata]
                if missing_mandatory:
                    details_log.append(f"For {content_type}, missing mandatory metadata: {missing_mandatory}.")
                    verdicts.append("metadata_incomplete")
                    confidence_scores.append(0.3)
                else:
                    details_log.append(f"All mandatory metadata for {content_type} present.")
            
            # Check for forbidden authors (example)
            if "author_must_not_be" in rules and "author" in metadata:
                if metadata["author"] in rules["author_must_not_be"]:
                    details_log.append(f"Author '{metadata['author']}' is on a forbidden list for {content_type}.")
                    verdicts.append("problematic_author")
                    confidence_scores.append(0.2)

            # Check for "should contain" (example for image/jpeg)
            if "metadata_should_contain" in rules:
                missing_should = [key for key in rules["metadata_should_contain"] if key not in metadata]
                if missing_should:
                     details_log.append(f"For {content_type}, recommended metadata missing: {missing_should}.")
                     # This might lower confidence but not necessarily lead to "unverified"
            
            if "metadata_flag_if_missing_all" in rules:
                all_missing = True
                for key in rules["metadata_flag_if_missing_all"]:
                    if key in metadata:
                        all_missing = False
                        break
                if all_missing:
                    details_log.append(f"For {content_type}, all key metadata fields ({rules['metadata_flag_if_missing_all']}) are missing.")
                    verdicts.append("significant_metadata_missing")
                    confidence_scores.append(0.25)


        # Determine overall verdict (simplified logic)
        final_verdict = "neutral_no_strong_signal" # Default if no strong signals
        if "suspicious_source" in verdicts or "problematic_author" in verdicts or "metadata_incomplete" in verdicts or "significant_metadata_missing" in verdicts:
            final_verdict = "caution_advised"
        elif confidence_scores and all(cs > 0.7 for cs in confidence_scores) and not verdicts: # Example for positive
            final_verdict = "appears_consistent_with_known_facts"

        # Calculate an average confidence (very naive for now)
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
        
        return self.generate_verification_event(
            verdict=final_verdict,
            details={"log": details_log, "triggered_verdicts": verdicts},
            confidence_score=round(avg_confidence, 2)
        )

if __name__ == '__main__':
    agent = KnownFactsAgent()
    print(f"\n--- Testing Agent: {agent.get_info()['agent_id']} ---")
    import json

    claim1 = {
        "claim_id": "fact_test_001",
        "submitter_id": "official_press_agency_001",
        "content_type": "application/pdf",
        "metadata": {"author": "John Doe", "creation_date": "2024-01-01"}
    }
    result1 = agent.verify_claim_data(claim1)
    print(f"\nResult for claim1:\n{json.dumps(result1, indent=2)}")

    claim2 = {
        "claim_id": "fact_test_002",
        "submitter_id": "unknown_blogger_77",
        "content_type": "image/jpeg",
        "metadata": {"source_url": "http://example.com/image.jpg"} # Missing camera, gps etc.
    }
    result2 = agent.verify_claim_data(claim2)
    print(f"\nResult for claim2:\n{json.dumps(result2, indent=2)}")
    
    claim3 = {
        "claim_id": "fact_test_003",
        "submitter_id": "known_disinfo_source_xyz",
        "content_type": "text/plain",
        "metadata": {}
    }
    result3 = agent.verify_claim_data(claim3)
    print(f"\nResult for claim3:\n{json.dumps(result3, indent=2)}")

    claim4 = {
        "claim_id": "fact_test_004",
        "submitter_id": "research_institute_alpha",
        "content_type": "application/pdf",
        "metadata": {"author": "anonymous_unverified", "creation_date": "2023-03-15"} # Problematic author
    }
    result4 = agent.verify_claim_data(claim4)
    print(f"\nResult for claim4:\n{json.dumps(result4, indent=2)}")