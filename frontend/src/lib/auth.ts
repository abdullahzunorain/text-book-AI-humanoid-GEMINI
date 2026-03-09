import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
});

export const { signIn, signUp, signOut, useSession } = authClient;
