# node/core_node.py

from .ledger import InMemoryLedger # Use a relative import
import datetime

class HeliosCoreNode:
    def __init__(self, node_id="helios_node_001"):
        self.node_id = node_id
        self.ledger = InMemoryLedger() # Each node instance will have its own ledger for MVP1
        self.ai_agents = {} # Placeholder for AI agents
        print(f"HeliosCoreNode '{self.node_id}' initialized.")
        self.ledger.display_ledger() # Display initial ledger state (genesis block)

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

    def trigger_verification(self, claim_id):
        """
        Placeholder for triggering AI agents to verify a claim.
        In MVP1, this will be very basic.
        """
        claim_data = self.ledger.get_claim_by_id(claim_id)
        if not claim_data:
            print(f"Error: Claim '{claim_id}' not found for verification.")
            return

        if claim_data["status"] != "pending_verification":
            print(f"Claim '{claim_id}' is not pending verification. Current status: {claim_data['status']}")
            return

        print(f"Node '{self.node_id}' initiating verification for claim '{claim_id}'...")
        
        # Simulate a very basic verification process for MVP1
        # In the future, this will call actual AI agents.
        verification_event = {
            "agent_id": "basic_verifier_mvp1",
            "timestamp": str(datetime.datetime.utcnow().isoformat()),
            "action": "initial_check",
            "result": "preliminary_pass", # or "preliminary_fail"
            "notes": "MVP1 basic check: content hash length > 5 assumed 'pass' for demo."
        }

        # Directly update the claim in the ledger (not how a real blockchain works, but fine for MVP1)
        for block in self.ledger.chain:
            if block["claim_data"].get("claim_id") == claim_id:
                block["claim_data"]["verification_history"].append(verification_event)
                # Simple rule for MVP1: if content_hash is longer than 5 chars, mark as 'verified_preliminary'
                if len(claim_data.get("content_hash", "")) > 5:
                    block["claim_data"]["status"] = "verified_preliminary"
                else:
                    block["claim_data"]["status"] = "failed_preliminary"
                print(f"Claim '{claim_id}' status updated to: {block['claim_data']['status']}")
                self.view_claim(claim_id) # Show the updated claim
                break
        else:
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