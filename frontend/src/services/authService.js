// Auth service (CP19): login / register / me, backed by /api/v1/auth.
import { api, tokenStore } from "./api";

export const authService = {
  async login(email, password) {
    const tokens = await api.post("/auth/login", { email, password }, false);
    tokenStore.set(tokens.access_token, tokens.refresh_token);
    return tokens;
  },
  async register(name, email, password) {
    return api.post("/auth/register", { name, email, password }, false);
  },
  async me() {
    return api.get("/auth/me");
  },
  logout() {
    // best-effort server logout; ignore failures
    api.post("/auth/logout", {}).catch(() => {});
    tokenStore.clear();
  },
  isLoggedIn() {
    return !!tokenStore.get();
  },
};
