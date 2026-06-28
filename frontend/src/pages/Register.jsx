// Register page (CP19): POST /auth/register; MOE-domain help text.
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authService } from "../services/authService";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input, Label } from "../components/ui/input";
import ErrorMessage from "../components/ErrorMessage";

export default function Register() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [ok, setOk] = useState(false);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e) {
    e.preventDefault();
    setError(null); setBusy(true);
    try {
      await authService.register(name, email, password);
      setOk(true);
      setTimeout(() => navigate("/login"), 1200);
    } catch (err) {
      setError(err.message || "Registration failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <Card className="w-full max-w-md">
        <CardHeader><CardTitle>Create account</CardTitle></CardHeader>
        <CardContent>
          <form onSubmit={onSubmit} className="space-y-4">
            <div>
              <Label>Full name</Label>
              <Input value={name} onChange={(e) => setName(e.target.value)} required />
            </div>
            <div>
              <Label>Email</Label>
              <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                     placeholder="name@moe.gov.my" required />
              <p className="mt-1 text-xs text-slate-500">
                Only <span className="font-medium">@moe.gov.my</span> and
                {" "}<span className="font-medium">@moe-dl.edu.my</span> accounts are permitted.
              </p>
            </div>
            <div>
              <Label>Password</Label>
              <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                     minLength={8} required />
              <p className="mt-1 text-xs text-slate-500">Minimum 8 characters.</p>
            </div>
            <ErrorMessage message={error} />
            {ok && <p className="text-sm text-green-700">Account created. Redirecting to login…</p>}
            <Button type="submit" className="w-full" disabled={busy}>
              {busy ? "Creating…" : "Register"}
            </Button>
          </form>
          <p className="mt-4 text-center text-sm text-slate-500">
            Have an account? <Link to="/login" className="text-blue-700 hover:underline">Sign in</Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
