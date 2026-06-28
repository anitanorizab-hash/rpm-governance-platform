// AuthContext (CP19): real auth — login/logout/current user, token + role storage.
import { createContext, useContext, useEffect, useState } from "react";
import { authService } from "../services/authService";
import { tokenStore } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // On mount, restore session from a stored token (fetch /auth/me).
  useEffect(() => {
    let active = true;
    async function restore() {
      if (!tokenStore.get()) { setLoading(false); return; }
      try {
        const me = await authService.me();
        if (active) setUser(me);
      } catch {
        tokenStore.clear();
      } finally {
        if (active) setLoading(false);
      }
    }
    restore();
    return () => { active = false; };
  }, []);

  async function login(email, password) {
    await authService.login(email, password);
    const me = await authService.me();
    setUser(me);
    return me;
  }

  function logout() {
    authService.logout();
    setUser(null);
  }

  const value = {
    user,
    roles: user?.roles || [],
    isAuthenticated: !!user,
    loading,
    login,
    logout,
    hasRole: (...roles) => (user?.roles || []).some((r) => roles.includes(r)),
  };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
