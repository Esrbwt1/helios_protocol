# main.py

from node.core_node import HeliosCoreNode # Use an absolute import from the project root
import time # For a slight delay in demo

def run_helios_node_demo():
    print("**********************************************")
    print("*      Welcome to Helios Protocol Node MVP1  *")
    print("**********************************************")
    print("\nInitializing a demo Helios Core Node...")
    
    node_instance = HeliosCoreNode(node_id="mvp1_demo_node")
    
    print("\n--- Demo Node Initialized ---")
    print(f"Node ID: {node_instance.node_id}")
    print("Registered AI Agents:")
    for agent_id, agent_instance in node_instance.ai_agents.items():
        print(f"  - {agent_id} (Version: {agent_instance.agent_version})")
    print("The ledger already contains the Genesis Block.")
    
    # --- Claim Set 1: Simple Text Claim ---
    print("\n\n--- Simulating Claim 1: Simple Text ---")
    claim1_content = "This is a basic statement for initial verification."
    claim1_hash = "text_sha256_placeholder_" + hex(hash(claim1_content))[2:]
    
    submitted_claim1_data = node_instance.submit_new_claim(
        content_hash=claim1_hash,
        content_type="text/plain",
        submitter_id="user_alice_generic", # Generic submitter
        metadata={"description": "A plain text document."}
    )
    
    if submitted_claim1_data:
        claim_id_1 = submitted_claim1_data['claim_id']
        print(f"Successfully submitted Claim ID: {claim_id_1}")
        time.sleep(0.1) # Small delay for readability of output
        node_instance.trigger_verification(claim_id_1)

    # --- Claim Set 2: Image Claim from a "Known Good" Submitter ---
    print("\n\n--- Simulating Claim 2: Image from Known Good Submitter ---")
    claim2_content = "Raw image data bytes would go here..."
    claim2_hash = "image_sha256_placeholder_" + hex(hash(claim2_content) + 1)[2:] # Ensure different hash
    
    submitted_claim2_data = node_instance.submit_new_claim(
        content_hash=claim2_hash,
        content_type="image/jpeg",
        submitter_id="official_press_agency_001", # Known good submitter in KnownFactsAgent
        metadata={
            "filename": "important_event.jpg", 
            "camera_model": "Professional DSLR MkIV",
            "gps_location": "40.7128N_74.0060W", # Example GPS
            "creation_software": "Photoshop v25"
        }
    )

    if submitted_claim2_data:
        claim_id_2 = submitted_claim2_data['claim_id']
        print(f"Successfully submitted Claim ID: {claim_id_2}")
        time.sleep(0.1)
        node_instance.trigger_verification(claim_id_2)

    # --- Claim Set 3: PDF Claim from a "Known Disinfo" Submitter ---
    print("\n\n--- Simulating Claim 3: PDF from Known Disinfo Submitter ---")
    claim3_content = "Content of a suspicious PDF document..."
    claim3_hash = "pdf_sha256_placeholder_" + hex(hash(claim3_content) + 2)[2:]
    
    submitted_claim3_data = node_instance.submit_new_claim(
        content_hash=claim3_hash,
        content_type="application/pdf", # KnownFactsAgent has rules for PDF
        submitter_id="known_disinfo_source_xyz", # Known bad submitter
        metadata={
            "author": "Anonymous Agitator", # Might be flagged if rules are stricter
            # Missing "creation_date" which KnownFactsAgent might look for in PDFs
        }
    )

    if submitted_claim3_data:
        claim_id_3 = submitted_claim3_data['claim_id']
        print(f"Successfully submitted Claim ID: {claim_id_3}")
        time.sleep(0.1)
        node_instance.trigger_verification(claim_id_3)
        
    # --- Claim Set 4: Text claim with very short hash ---
    print("\n\n--- Simulating Claim 4: Text with short hash ---")
    claim4_content = "Short content."
    claim4_hash = "shorthash" # This should be flagged by SimpleVerifierAgent
    
    submitted_claim4_data = node_instance.submit_new_claim(
        content_hash=claim4_hash,
        content_type="text/plain",
        submitter_id="user_bob_quickpost",
        metadata={"notes": "A quick note with a deliberately short hash."}
    )
    
    if submitted_claim4_data:
        claim_id_4 = submitted_claim4_data['claim_id']
        print(f"Successfully submitted Claim ID: {claim_id_4}")
        time.sleep(0.1)
        node_instance.trigger_verification(claim_id_4)


    # Display the final state of the ledger on this node
    print("\n\n--- Final Ledger State on this Node ---")
    node_instance.view_entire_ledger()
    
    print("\n**********************************************")
    print("*        Helios Node MVP1 Demo Complete      *")
    print("**********************************************")

if __name__ == "__main__":
    run_helios_node_demo()