# node/core_node.py

from .ledger import InMemoryLedger # Use a relative import
import datetime
from agents.simple_verifier_agent import SimpleVerifierAgent # New import

class HeliosCoreNode:
    def __init__(self, node_id="helios_node_001"):
        self.node_id = node_id
        self.ledger = InMemoryLedger() # Each node instance will have its own ledger for MVP1
        self.ai_agents = {} 
        self._register_default_agents() # New method call
        print(f"HeliosCoreNode '{self.node_id}' initialized.")
        self.ledger.display_ledger() # Display initial ledger state (genesis block)
    
    def _register_default_agents(self):
        """
        Registers default AI agents available to this node.
        """
        simple_agent = SimpleVerifierAgent()
        self.register_ai_agent(simple_agent.agent_id, simple_agent)

    def submit_new_claim(self, content_hash, content_type, submitter_id, metadata=None):
        """
        Allows submission of a new claim to this node's ledger.
        """
        if not all([content_hash, content_type, submitter_id]):
            print("Error: content_hash, content_type, and submitter_id are required.")
            return None

        claim_id = f"claim_{self.node_id}_{len(self.ledger.chain)}_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        new_claim_data = {
            "claim_id": claim_id,
            "timestamp": str(datetime.datetime.utcnow().isoformat()),
            "submitter_id": submitter_id,
            "content_hash": content_hash,
            "content_type": content_type,
            "metadata": metadata if metadata else {},
            "verification_history": [], # Will be populated by AI agents later
            "status": "pending_verification" # Initial status
        }
        
        block = self.ledger.add_claim(new_claim_data)
        if block:
            print(f"Node '{self.node_id}' successfully submitted claim '{claim_id}' to its ledger.")
            # In a real system, this claim would be broadcast to the network.
            # For MVP1, it's just local to this node's ledger.
            return new_claim_data
        else:
            print(f"Node '{self.node_id}' failed to submit claim to its ledger.")
            return None

    def view_claim(self, claim_id):
        """
        Retrieves and displays a specific claim from the ledger.
        """
        claim_data = self.ledger.get_claim_by_id(claim_id)
        if claim_data:
            print(f"\n--- Viewing Claim '{claim_id}' on Node '{self.node_id}' ---")
            import json
            print(json.dumps(claim_data, indent=2))
            print("--- End of Claim View ---")
            return claim_data
        else:
            print(f"Claim '{claim_id}' not found on Node '{self.node_id}'.")
            return None

    def view_entire_ledger(self):
        """
        Displays the entire ledger content for this node.
        """
        print(f"\n--- Full Ledger View for Node '{self.node_id}' ---")
        self.ledger.display_ledger()

    # Placeholder for AI agent interaction
    def register_ai_agent(self, agent_id, agent_instance):
        self.ai_agents[agent_id] = agent_instance
        print(f"AI Agent '{agent_id}' registered with Node '{self.node_id}'.")

    def trigger_verification(self, claim_id, agent_id=None):
        """
        Triggers registered AI agents to verify a claim.
        If agent_id is specified, only that agent is used.
        Otherwise, all agents that support the claim's content type are triggered.
        """
        claim_data = self.ledger.get_claim_by_id(claim_id)
        if not claim_data:
            print(f"Error: Claim '{claim_id}' not found for verification on Node '{self.node_id}'.")
            return

        if claim_data["status"] != "pending_verification" and claim_data["status"] != "reverification_needed":
            print(f"Claim '{claim_id}' is not pending_verification or reverification_needed. Current status: {claim_data['status']}")
            # Optionally, allow re-verification if needed
            # return 

        print(f"Node '{self.node_id}' initiating verification for claim '{claim_id}'...")
        
        verification_results_for_claim = []
        agents_to_run = []

        if agent_id:
            if agent_id in self.ai_agents:
                agents_to_run.append(self.ai_agents[agent_id])
            else:
                print(f"Warning: Specified agent_id '{agent_id}' not found on node '{self.node_id}'.")
        else: # Run all applicable agents
            for ag_id, agent_instance in self.ai_agents.items():
                if agent_instance.can_verify(claim_data.get("content_type")):
                    agents_to_run.append(agent_instance)
        
        if not agents_to_run:
            print(f"No suitable AI agents found or specified to verify claim '{claim_id}' (content_type: {claim_data.get('content_type')}).")
            # Potentially mark as "unable_to_verify_no_agent"
            return

        for agent in agents_to_run:
            print(f"--- Running Agent: {agent.agent_id} v{agent.agent_version} ---")
            try:
                # For MVP1, we're not passing actual claim_content yet.
                # This will be important when agents need to analyze the content itself.
                verification_result = agent.verify_claim_data(claim_data, claim_content=None)
                verification_results_for_claim.append(verification_result)
                print(f"Agent '{agent.agent_id}' completed. Verdict: {verification_result.get('verdict')}")
            except Exception as e:
                print(f"Error running agent '{agent.agent_id}': {e}")
                error_result = {
                    "agent_id": agent.agent_id,
                    "agent_version": agent.agent_version,
                    "timestamp": str(datetime.datetime.utcnow().isoformat()),
                    "verdict": "error_agent_execution",
                    "details": str(e)
                }
                verification_results_for_claim.append(error_result)

        # Update the claim in the ledger with the verification history
        # This is a simplified update for MVP1. A real DLT would handle this differently.
        updated_in_ledger = False
        for block_idx, block in enumerate(self.ledger.chain):
            if block["claim_data"].get("claim_id") == claim_id:
                # Append new verification events, don't overwrite existing ones
                if "verification_history" not in self.ledger.chain[block_idx]["claim_data"]:
                    self.ledger.chain[block_idx]["claim_data"]["verification_history"] = []
                
                for res in verification_results_for_claim:
                     self.ledger.chain[block_idx]["claim_data"]["verification_history"].append(res)
                
                # Determine overall status based on results (simplified logic for MVP1)
                # If any agent gives a "verified_preliminary", we'll use that.
                # More complex consensus logic will be needed later.
                final_verdict = "pending_verification" # Default if no conclusive results
                highest_confidence = 0.0
                
                for res in self.ledger.chain[block_idx]["claim_data"]["verification_history"]:
                    if res.get("verdict") == "verified_preliminary":
                        final_verdict = "verified_preliminary"
                        # confidence = res.get("confidence_score", 0)
                        # if confidence > highest_confidence: # Example of using confidence
                        #    highest_confidence = confidence
                        break # For MVP, first "verified_preliminary" is enough
                    elif res.get("verdict") == "unverified":
                        final_verdict = "unverified" 
                        # Could also break here or collect all verdicts

                self.ledger.chain[block_idx]["claim_data"]["status"] = final_verdict
                updated_in_ledger = True
                print(f"Claim '{claim_id}' status updated to: {final_verdict} after agent processing.")
                self.view_claim(claim_id) # Show the updated claim
                break
        
        if not updated_in_ledger:
             print(f"Error: Could not find claim '{claim_id}' in ledger to update status after verification attempt.")


if __name__ == '__main__':
    # Test the HeliosCoreNode
    print("--- Starting HeliosCoreNode Test ---")
    my_node = HeliosCoreNode(node_id="test_node_alpha")
    
    print("\n--- Submitting a new claim ---")
    claim1_data = my_node.submit_new_claim(
        content_hash="abcdef1234567890",
        content_type="image/jpeg",
        submitter_id="user_beta",
        metadata={"filename": "sunset.jpg", "camera_model": "Pixel 8 Pro"}
    )

    if claim1_data:
        print(f"\n--- Viewing the submitted claim by ID: {claim1_data['claim_id']} ---")
        my_node.view_claim(claim1_data["claim_id"])

        print(f"\n--- Triggering verification for claim: {claim1_data['claim_id']} ---")
        my_node.trigger_verification(claim1_data["claim_id"])
    
    print("\n--- Submitting another new claim (short hash for different verification outcome) ---")
    claim2_data = my_node.submit_new_claim(
        content_hash="xyz", # short hash
        content_type="text/plain",
        submitter_id="user_gamma",
        metadata={"source": "internal_note"}
    )

    if claim2_data:
        print(f"\n--- Triggering verification for claim: {claim2_data['claim_id']} ---")
        my_node.trigger_verification(claim2_data["claim_id"])

    print("\n--- Displaying full ledger for the node ---")
    my_node.view_entire_ledger()
    
    print("\n--- Test Viewing Genesis Claim ---")
    my_node.view_claim("genesis_000")

    print("\n--- Test Viewing Non-Existent Claim ---")
    my_node.view_claim("claim_does_not_exist_123")

    print("\n--- End of HeliosCoreNode Test ---")