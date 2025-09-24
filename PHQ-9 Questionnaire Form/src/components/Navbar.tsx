import React from "react";
import { Button } from "./ui/button";
import { Heart, Menu } from "lucide-react";

export function Navbar({
	user,
	onLogout,
	onShowRegister,
}: {
	user: { user_id: string; username: string } | null;
	onLogout: () => void;
	onShowRegister: () => void;
}) {
	return (
		<nav className="bg-blue-600 shadow-lg">
			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<div className="flex justify-between items-center h-16">
					{/* Logo and Brand */}
					<div className="flex items-center space-x-3">
						<div className="bg-blue-500 p-2 rounded-full">
							<Heart className="h-6 w-6 text-white" />
						</div>
						<div>
							<h1 className="text-white text-xl font-semibold">
								MindCare
							</h1>
							<p className="text-white/80 text-sm">
								Mental Health Assessment
							</p>
						</div>
					</div>
					<div className="hidden md:flex items-center space-x-6">
						{!user ? (
							<>
								<Button
									variant="ghost"
									className="text-white hover:bg-blue-500 hover:text-white"
									onClick={onShowRegister}
								>
									Register
								</Button>
							</>
						) : (
							<>
								<span className="text-white font-semibold">
									{user.username}
								</span>
								<Button
									variant="ghost"
									className="text-white hover:bg-blue-500 hover:text-white"
									onClick={onLogout}
								>
									Logout
								</Button>
							</>
						)}
					</div>
					{/* Mobile menu button */}
					<div className="md:hidden">
						<Button
							variant="ghost"
							size="sm"
							className="text-white hover:bg-blue-500"
						>
							<Menu className="h-6 w-6" />
						</Button>
					</div>
				</div>
			</div>
		</nav>
	);
}
