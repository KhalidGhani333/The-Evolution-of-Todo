Skill Name: StatelessArchitectureSkill
Purpose:
Ensure stateless server design patterns for scalability.

Capabilities:
Design endpoints without in-memory state
Store all state in database
Enable horizontal scaling
Implement idempotent operations
Handle concurrent requests safely
Design for server restart resilience

Usage Rules:
Applied to all Phase III backend components
No global variables for user state
No session storage in memory
All conversation state in database
Each request must be self-contained
Critical for production deployment and Kubernetes
