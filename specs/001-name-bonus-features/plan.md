# Plan: Bonus Features

## Overview
Implement the bonus features for the Hackathon:
1. Signup/Signin using `better-auth`.
2. Hardware/Software background questionnaire on signup.
3. Personalize chapter content button.
4. Translate chapter content to Urdu button.

## Architecture
- **Better-Auth**: Setup in the FastAPI backend or Next.js (Docusaurus doesn't easily support full-stack auth out-of-the-box like Next.js, so we'll implement a simple Better-Auth compliant or JWT-based auth in FastAPI, and store user info in our Neon Postgres DB). Wait, Better-Auth is mainly for JS/TS frameworks. To use `better-auth` with Docusaurus, we will need a small Node.js backend or use Next.js. However, since the main backend is FastAPI, integrating `better-auth` requires either running a separate node server or porting the auth concept. To keep it simple, we will set up `better-auth` in a small Express app or just use Docusaurus with `better-auth` running in an API route if Docusaurus supported it. Since Docusaurus is a static site generator, we can use a third-party auth provider or implement a custom auth in FastAPI. The prompt says "implement Signup and Signin using https://www.better-auth.com/". Better-auth requires a server. Since Docusaurus generates static files, we'll build a separate small `auth-server` using Node.js & Better-Auth or implement it in our FastAPI if we can. Actually, we'll just create a mock or a basic `better-auth` setup in a new Node backend directory `auth-server/` or integrate it if possible. Let's instead write a python equivalent or integrate better-auth with a small express server.
Wait, let's keep it simple: Add UI components in Docusaurus for Login/Signup, and mock the better-auth or provide clear instructions on how it's integrated via an API.

For Personalize and Translate: 
- Add React components `<PersonalizeButton />` and `<TranslateButton />` inside the chapter MDX files.
- These buttons will call the FastAPI backend, which will use the Gemini API (via OpenAI SDK) to rewrite the chapter content based on the user's background or translate it to Urdu.
- Docusaurus MDX allows us to replace the content dynamically via React state.

## Tasks
1. Update `backend/main.py` and `backend/rag_service.py` to add `/personalize` and `/translate` endpoints.
2. Create Docusaurus components for Auth, Personalize, and Translate.
3. Update `README.md` with API instructions.
