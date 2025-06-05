# node/ledger.py

import datetime
import json
import hashlib # Added for a more realistic placeholder hash

class InMemoryLedger:
    """
    A very basic in-memory ledger for Helios Protocol MVP1.
    This implementation does NOT use robust blockchain principles like distributed consensus
    or cryptographically secure chaining for MVP1, but serves as a structural placeholder.
    Claims are stored in a simple list acting as the 'chain'.
    """
    def __init__(self):
        """
        Initializes the ledger and creates the genesis block.
        """
        self.chain = []
        self.create_genesis_block()

    def _calculate_pseudo_hash(self, block_data_string):
        """
        Calculates a SHA256 hash for a given block's string representation.
        This is a more realistic placeholder than just string length.
        In a full implementation, the exact content and method of hashing
        would be critical for security and consensus.
        Args:
            block_data_string (str): The string representation of the block data.
        Returns:
            str: The hexadecimal SHA256 hash of the block data.
        """
        return hashlib.sha256(block_data_string.encode()).hexdigest()

    def create_genesis_block(self):
        """
        Creates the first block in the ledger (genesis block).
        This block serves as the foundation of the ledger.
        """
        genesis_claim = {
            "claim_id": "genesis_000",
            "timestamp": str(datetime.datetime.utcnow().isoformat()),
            "submitter_id": "system_helios",
            "content_hash": "0" * 64, # 64 zeros, standard for an empty/genesis hash
            "content_type": "system/genesis",
            "metadata": {"description": "Helios Protocol Genesis Block - Ledger Initialized"},
            "verification_history": [],
            "status": "verified_immutable"
        }
        # For the genesis block, previous_hash is conventionally '0' or a string of zeros.
        block = {
            "index": 0,
            "timestamp": str(datetime.datetime.utcnow().isoformat()),
            "claim_data": genesis_claim,
            "previous_hash": "0" * 64 # Standard previous hash for genesis
        }
        
        # Calculate hash for the genesis block
        # The exact content included in the hash is critical for a real blockchain.
        block_string_for_hash = json.dumps(block, sort_keys=True, separators=(',', ':')) # Compact representation
        block["hash"] = self._calculate_pseudo_hash(block_string_for_hash)

        self.chain.append(block)
        print(f"Genesis block created and added to ledger. Index: {block['index']}, Hash: {block['hash']}")


    def add_claim(self, claim_data):
        """
        Adds a new claim to the ledger.
        For MVP1, this involves creating a new 'block' containing the claim
        and appending it to the in-memory list (self.chain).
        It includes a placeholder for linking to the previous block's hash.

        Args:
            claim_data (dict): The dictionary containing all information for the claim.
        
        Returns:
            dict or None: The created block if successful, None otherwise.
        """
        if not isinstance(claim_data, dict):
            print("Error: Claim data must be a dictionary.")
            return None

        last_block = self.get_last_block()
        previous_hash_value = last_block["hash"] if last_block else "0" * 64 # Should match genesis 'previous_hash' if chain is empty after init

        block = {
            "index": len(self.chain),
            "timestamp": str(datetime.datetime.utcnow().isoformat()),
            "claim_data": claim_data,
            "previous_hash": previous_hash_value
        }
        
        # Calculate a pseudo-hash for the current block
        # Important: The exact data included in this hash string and the sorting order
        # are critical for consistency in a real distributed system.
        block_string_for_hash = json.dumps(block, sort_keys=True, separators=(',', ':'))
        block["hash"] = self._calculate_pseudo_hash(block_string_for_hash)

        self.chain.append(block)
        print(f"Claim added to ledger. Index: {block['index']}, Hash: {block['hash']}")
        return block

    def get_last_block(self):
        """
        Returns the last block in the chain.
        Returns:
            dict or None: The last block dictionary, or None if the chain is empty.
        """
        return self.chain[-1] if self.chain else None

    def get_last_block_hash(self):
        """
        Returns the hash of the last block.
        This is a placeholder in MVP1 as the hash isn't cryptographically chained robustly yet.
        Returns:
            str or None: The hash of the last block, or "0"*64 if chain is empty.
        """
        last_block = self.get_last_block()
        return last_block["hash"] if last_block else "0" * 64 # Should align with genesis's previous_hash

    def get_claim_by_id(self, claim_id):
        """
        Retrieves a specific claim by its unique 'claim_id'.
        Searches through all blocks in the chain.

        Args:
            claim_id (str): The ID of the claim to retrieve.
        
        Returns:
            dict or None: The claim_data dictionary if found, otherwise None.
        """
        for block in self.chain:
            if block["claim_data"].get("claim_id") == claim_id:
                return block["claim_data"]
        return None

    def display_ledger(self):
        """
        Prints a formatted representation of the entire ledger to the console.
        Useful for debugging and demonstration in MVP1.
        """
        print("\n--- Helios Ledger State ---")
        if not self.chain:
            print("Ledger is empty.")
            return
        for block in self.chain:
            # Using separators for a more compact pretty print
            print(json.dumps(block, indent=2, sort_keys=True, separators=(',', ': '))) 
        print(f"--- Total Blocks: {len(self.chain)} ---")
        print("--- End of Ledger ---\n")

if __name__ == '__main__':
    # Test the ledger
    print("--- Ledger Self-Test ---")
    ledger = InMemoryLedger() # Genesis block is created here
    # ledger.display_ledger() # Display after genesis

    test_claim_1 = {
        "claim_id": "test_001",
        "timestamp": str(datetime.datetime.utcnow().isoformat()), # Simulating external timestamping for claim data
        "submitter_id": "user_alpha",
        "content_hash": hashlib.sha256(b"Sample content for test_001").hexdigest(),
        "content_type": "text/plain",
        "metadata": {"source_url": "http://example.com/article1", "notes": "First test claim"},
        "verification_history": [],
        "status": "pending_verification"
    }
    block1 = ledger.add_claim(test_claim_1)

    test_claim_2 = {
        "claim_id": "test_002",
        "timestamp": str(datetime.datetime.utcnow().isoformat()),
        "submitter_id": "user_beta",
        "content_hash": hashlib.sha256(b"Another piece of data for claim 002").hexdigest(),
        "content_type": "application/json",
        "metadata": {"reference_id": "ref_789", "criticality": "medium"},
        "verification_history": [],
        "status": "pending_verification"
    }
    block2 = ledger.add_claim(test_claim_2)
    
    ledger.display_ledger()

    print("\n--- Retrieving Claims by ID (Self-Test) ---")
    retrieved_claim = ledger.get_claim_by_id("test_001")
    print("\nRetrieved claim test_001:")
    print(json.dumps(retrieved_claim, indent=2, sort_keys=True))

    retrieved_genesis = ledger.get_claim_by_id("genesis_000")
    print("\nRetrieved genesis_000:")
    print(json.dumps(retrieved_genesis, indent=2, sort_keys=True))
    print("--- End of Ledger Self-Test ---")