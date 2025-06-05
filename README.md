# Helios Protocol - MVP1

Helios Protocol is an experimental project aiming to build a decentralized truth and provenance layer for digital information.

This repository contains the Minimum Viable Product (MVP1) of a Helios Node. MVP1 is a locally runnable demonstration of core concepts, including:
*   A basic in-memory ledger for storing "claims" about digital content.
*   A node structure that manages claims and interacts with verification agents.
*   A simple, extensible framework for "AI" Verification Agents.
*   Two initial rule-based verification agents:
    *   SimpleVerifierAgent: Performs a basic check on content hash presence and length.
    *   KnownFactsAgent: Checks claim metadata against a predefined set of "known submitters" and content-type rules.

This is an early-stage research and development project. It is NOT yet a secure, decentralized, or production-ready system.

## Vision
The long-term vision for Helios Protocol is to create a universally adopted, open-source, AI-enhanced decentralized protocol to establish the provenance, veracity, and contextual truthfulness of digital information (text, images, videos, data). This aims to combat misinformation and build a more trustworthy digital ecosystem.

## Current Status (MVP1)
*   Local Operation Only: The current node runs as a standalone process. There is no peer-to-peer networking or distributed consensus yet.
*   In-Memory Ledger: Claim data is stored in memory and is lost when the program stops.
*   Rule-Based "AI" Agents: The current verification agents use simple predefined rules, not actual machine learning models.
*   Basic Hashing: A SHA256 hash is used for block pseudo-identity, but a full, secure blockchain hashing and chaining mechanism is not yet implemented.

## Getting Started (Running MVP1 Locally)

### Prerequisites
*   Python 3.8+
*   Git

### Setup
1.  Clone this repository:
    
    git clone <repository_url_will_go_here_once_on_github>
    cd helios_protocol
    
2.  (Optional but recommended) Create and activate a virtual environment:
    
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    
3.  There are no external package dependencies for MVP1 beyond the Python standard library.

### Running the Demo
Execute the main script from the project root directory:
python main.py

This will initialize a demo node, submit several sample claims, and run the registered verification agents against them. The output will show the process and the final state of the local ledger.

# Project Structure

    helios_protocol/
    ├── .gitignore         # Files and directories to ignore for Git
    ├── main.py            # Main entry point for the MVP1 demo
    ├── README.md          # This file
    ├── agents/            # Contains verification agent implementations
    │   ├── __init__.py
    │   ├── base_agent.py  # Abstract base class for all agents
    │   ├── simple_verifier_agent.py
    │   └── known_facts_agent.py
    └── node/              # Contains core node logic
        ├── __init__.py
        ├── core_node.py   # HeliosCoreNode class
        └── ledger.py      # InMemoryLedger class

# Next Steps (Beyond MVP1 - Future Vision for Phase 2 & 3)

* Phase 2 (Current Focus):

    * Open source the MVP1 codebase (this repository).
    * Develop a basic Testnet concept (e.g., simple client-server interaction between a few nodes).
    * Enhance documentation and create initial community channels.
    * Refine the core protocol whitepaper.

* Phase 3 & Beyond:

    * Implement persistent storage for the ledger (e.g., SQLite, then potentially a proper DLT).
    * Develop P2P networking capabilities for node communication.
    * Design and implement a basic consensus mechanism.
    * Integrate actual machine learning models into more advanced AI Verification Agents.
    * Develop a formal Helios Protocol specification.
    * Build tools for content registration and verification.

# How to Contribute (Future)
Once community channels are established, contribution guidelines will be provided. For now, feel free to explore the code. Feedback is welcome once an official communication channel is announced.

## Community & Communication

This project is in its very early stages. Initial channels for questions, feedback, and discussion are:

*   GitHub Issues: For bug reports, feature requests, and specific technical questions related to the code. Please check existing issues before creating a new one. https://github.com/Esrbwt1/helios_protocol/issues
*   GitHub Discussions: (If you enabled it) For general Q&A, broader ideas, and community discussions. https://github.com/Esrbwt1/helios_protocol/discussions

As the community grows, additional channels may be established.

# License
(To be decided - Likely MIT or Apache 2.0 for the open-source code)
This project is in active early development. Features and architecture are subject to change.
