# main.py

from node.core_node import HeliosCoreNode # Use an absolute import from the project root

def run_helios_node_demo():
    print("**********************************************")
    print("*      Welcome to Helios Protocol Node MVP1  *")
    print("**********************************************")
    print("\nInitializing a demo Helios Core Node...")
    
    # Create an instance of our node
    # You can give it a unique ID if you like
    node_instance = HeliosCoreNode(node_id="mvp1_demo_node")
    
    print("\n--- Demo Node Initialized ---")
    print(f"Node ID: {node_instance.node_id}")
    print("The ledger already contains the Genesis Block.")
    
    # Example: Simulate submitting a few claims
    print("\n--- Simulating Claim Submissions ---")
    
    claim1_content = "This is the content of the first test document."
    # In a real scenario, content_hash would be a cryptographic hash (e.g., SHA256)
    # For MVP1, we'll use a simplified representation.
    claim1_hash = "sha256_placeholder_" + hex(hash(claim1_content))[2:] # Simple hash for demo
    
    submitted_claim1 = node_instance.submit_new_claim(
        content_hash=claim1_hash,
        content_type="text/plain",
        submitter_id="demo_user_alice",
        metadata={"description": "First test document submission."}
    )
    
    if submitted_claim1:
        print(f"Successfully submitted Claim ID: {submitted_claim1['claim_id']}")
        node_instance.trigger_verification(submitted_claim1['claim_id'])


    claim2_content = "Another piece of important information."
    claim2_hash = "sha256_placeholder_" + hex(hash(claim2_content))[2:]

    submitted_claim2 = node_instance.submit_new_claim(
        content_hash=claim2_hash, # A different hash
        content_type="application/json",
        submitter_id="demo_user_bob",
        metadata={"source_app": "DemoApp v0.1", "notes": "This content is critical."}
    )

    if submitted_claim2:
        print(f"Successfully submitted Claim ID: {submitted_claim2['claim_id']}")
        # Let's try to verify this one too
        node_instance.trigger_verification(submitted_claim2['claim_id'])

    # Display the final state of the ledger on this node
    print("\n--- Final Ledger State on this Node ---")
    node_instance.view_entire_ledger()
    
    print("\n**********************************************")
    print("*        Helios Node MVP1 Demo Complete      *")
    print("**********************************************")

if __name__ == "__main__":
    run_helios_node_demo()