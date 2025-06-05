# node/ledger.py

import datetime
import json

class InMemoryLedger:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Creates the first block in the ledger (genesis block).
        """
        genesis_claim = {
            "claim_id": "genesis_000",
            "timestamp": str(datetime.datetime.utcnow().isoformat()),
            "submitter_id": "system_helios",
            "content_hash": "0" * 64, # 64 zeros
            "content_type": "system",
            "metadata": {"description": "Helios Protocol Genesis Block"},
            "verification_history": [],
            "status": "verified_immutable"
        }
        self.add_claim(genesis_claim, is_genesis=True)

    def add_claim(self, claim_data, is_genesis=False):
        """
        Adds a new claim to the ledger.
        For MVP1, we are not implementing complex block creation or consensus.
        We're just appending to a list.
        """
        if not isinstance(claim_data, dict):
            print("Error: Claim data must be a dictionary.")
            return None

        block = {
            "index": len(self.chain),
            "timestamp": str(datetime.datetime.utcnow().isoformat()),
            "claim_data": claim_data,
            "previous_hash": self.get_last_block_hash() if not is_genesis and self.chain else "0"
        }
        
        # In a real blockchain, this hash would be complex. Here, it's simple.
        block_string = json.dumps(block, sort_keys=True).encode()
        # We'll need a proper hashing function later. For now, just use length as a placeholder.
        # This is NOT cryptographically secure and is ONLY for MVP structure.
        current_hash_placeholder = str(len(block_string)) 

        block["hash"] = current_hash_placeholder # Placeholder hash

        self.chain.append(block)
        print(f"Claim added to ledger. Index: {block['index']}")
        return block

    def get_last_block(self):
        """
        Returns the last block in the chain.
        """
        return self.chain[-1] if self.chain else None

    def get_last_block_hash(self):
        """
        Returns the hash of the last block. Placeholder for now.
        """
        last_block = self.get_last_block()
        return last_block["hash"] if last_block else "0"

    def get_claim_by_id(self, claim_id):
        """
        Retrieves a claim by its ID.
        """
        for block in self.chain:
            if block["claim_data"].get("claim_id") == claim_id:
                return block["claim_data"]
        return None

    def display_ledger(self):
        """
        Prints the entire ledger to the console.
        """
        print("\n--- Helios Ledger State ---")
        if not self.chain:
            print("Ledger is empty.")
            return
        for block in self.chain:
            print(json.dumps(block, indent=2))
        print("--- End of Ledger ---\n")

if __name__ == '__main__':
    # Test the ledger
    ledger = InMemoryLedger()
    ledger.display_ledger()

    test_claim_1 = {
        "claim_id": "test_001",
        "timestamp": str(datetime.datetime.utcnow().isoformat()),
        "submitter_id": "user_alpha",
        "content_hash": "a1b2c3d4e5f6...", # Placeholder
        "content_type": "text/plain",
        "metadata": {"source_url": "http://example.com/article1"},
        "verification_history": [],
        "status": "pending_verification"
    }
    ledger.add_claim(test_claim_1)
    ledger.display_ledger()

    retrieved_claim = ledger.get_claim_by_id("test_001")
    print("\nRetrieved claim test_001:")
    print(json.dumps(retrieved_claim, indent=2))

    retrieved_genesis = ledger.get_claim_by_id("genesis_000")
    print("\nRetrieved genesis_000:")
    print(json.dumps(retrieved_genesis, indent=2))