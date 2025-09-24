import React, { useState } from "react";
import { PHQ9Form } from "./components/PHQ9Form";
import { Navbar } from "./components/Navbar";
import Login from "./components/Login";
import Register from "./components/Register";

export default function App() {
	const [user, setUser] = useState<{
		user_id: string;
		username: string;
	} | null>(null);
	const [showRegister, setShowRegister] = useState(false);

	const handleLogout = () => {
		setUser(null);
		setShowRegister(false);
		localStorage.removeItem("user_id");
		localStorage.removeItem("username");
	};

	const handleLogin = (user: { user_id: string; username: string }) => {
		setUser(user);
		localStorage.setItem("user_id", user.user_id);
		localStorage.setItem("username", user.username);
	};

	const handleRegister = () => {
		setShowRegister(false);
	};

	React.useEffect(() => {
		// Persist login
		const user_id = localStorage.getItem("user_id");
		const username = localStorage.getItem("username");
		if (user_id && username) setUser({ user_id, username });
	}, []);

	return (
		<div className="min-h-screen bg-blue-50">
			<Navbar
				user={user}
				onLogout={handleLogout}
				onShowRegister={() => setShowRegister(true)}
			/>
			<main className="py-8">
				{!user ? (
					showRegister ? (
						<Register onRegister={handleRegister} />
					) : (
						<Login onLogin={handleLogin} />
					)
				) : (
					<PHQ9Form user_id={user.user_id} />
				)}
			</main>
			{/* Decorative background elements */}
			<div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
				<div className="absolute top-10 left-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
				<div className="absolute top-40 right-10 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
				<div className="absolute bottom-10 left-20 w-72 h-72 bg-blue-100 rounded-full mix-blend-multiply filter blur-xl opacity-25 animate-pulse animation-delay-4000"></div>
				<div className="absolute bottom-40 right-20 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-pulse animation-delay-6000"></div>
			</div>
		</div>
	);
}
