import React, { useState } from "react";
import {
	Card,
	CardHeader,
	CardTitle,
	CardDescription,
	CardContent,
} from "./ui/card";
import { Button } from "./ui/button";
import { Lock, Mail } from "lucide-react";

export default function Login({
	onLogin,
}: {
	onLogin: (user: { user_id: string; username: string }) => void;
}) {
	const [emailid, setEmailid] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError("");
		try {
			const res = await fetch("http://localhost:5000/api/login", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ emailid, password }),
			});
			const data = await res.json();
			if (!res.ok) throw new Error(data.error || "Login failed");
			onLogin(data);
		} catch (err: any) {
			setError(err.message);
		}
	};

	return (
		<div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100 py-12">
			<Card className="w-full max-w-md shadow-2xl border-0 bg-white">
				<CardHeader className="bg-blue-600 text-white rounded-t-lg">
					<CardTitle className="text-2xl flex items-center gap-3">
						<Lock className="h-6 w-6" /> Login
					</CardTitle>
					<CardDescription className="text-blue-100 text-lg">
						Welcome back! Please login to continue.
					</CardDescription>
				</CardHeader>
				<CardContent>
					<form onSubmit={handleSubmit} className="space-y-6 mt-2">
						{error && (
							<div className="mb-4 text-red-600 font-semibold">
								{error}
							</div>
						)}
						<div>
							<label className="block mb-1 font-medium">
								Email
							</label>
							<div className="relative">
								<span className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400">
									<Mail className="h-5 w-5" />
								</span>
								<input
									type="email"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={emailid}
									onChange={(e) => setEmailid(e.target.value)}
									required
								/>
							</div>
						</div>
						<div>
							<label className="block mb-1 font-medium">
								Password
							</label>
							<div className="relative">
								<span className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400">
									<Lock className="h-5 w-5" />
								</span>
								<input
									type="password"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={password}
									onChange={(e) =>
										setPassword(e.target.value)
									}
									required
								/>
							</div>
						</div>
						<Button
							type="submit"
							className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg shadow-lg transform transition-all duration-200 hover:scale-105"
						>
							Login
						</Button>
					</form>
				</CardContent>
			</Card>
		</div>
	);
}
