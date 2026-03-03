# Specification: Physical AI & Humanoid Robotics Textbook (MVP)

## 1. Overview
The goal is to create a unified AI-native textbook project for the "Physical AI & Humanoid Robotics" course. This includes a structured Docusaurus site and an integrated RAG-based chatbot.

## 2. Core Deliverables
- **Docusaurus Textbook:** A professional documentation site containing the course content.
- **RAG Chatbot:** A Retrieval-Augmented Generation chatbot embedded in the site.

## 3. Detailed Requirements

### 3.1. Textbook Content (Docusaurus)
The textbook must be structured into four primary modules:
1.  **Module 1: The Robotic Nervous System (ROS 2)** - Middleware, nodes, topics, services, rclpy, and URDF.
2.  **Module 2: The Digital Twin (Gazebo & Unity)** - Physics simulation, environments, sensors (LiDAR, IMU), and human-robot interaction.
3.  **Module 3: The AI-Robot Brain (NVIDIA Isaac™)** - Advanced perception, Isaac Sim, Isaac ROS (VSLAM/Nav2), and synthetic data.
4.  **Module 4: Vision-Language-Action (VLA)** - LLMs and Robotics, Whisper for voice, and the Autonomous Humanoid Capstone Project.

### 3.2. RAG Chatbot Integration
- **Stack:** FastAPI, OpenAI Agents, Neon (Postgres), and Qdrant (Vector DB).
- **Capability:** Answer user questions based *only* on the textbook's content.
- **Interface:** A chat UI embedded within the Docusaurus site.

## 4. Technical Stack
- **Frontend:** Docusaurus (React), Vanilla CSS.
- **Backend:** Python (FastAPI).
- **Database:** Neon Serverless Postgres.
- **Vector Search:** Qdrant Cloud.
- **AI Models:** Gemini (using API's).

## 5. Acceptance Criteria
- [ ] Docusaurus site initialized and deployed.
- [ ] Four modules populated with baseline content.
- [ ] FastAPI backend running and connected to Neon/Qdrant.
- [ ] RAG chatbot correctly retrieves information from the textbook.
- [ ] Search results are restricted to the book's context.

## 6. Future Scope (Phase 2)
- Better-auth integration.
- Content personalization.
- Urdu translation.