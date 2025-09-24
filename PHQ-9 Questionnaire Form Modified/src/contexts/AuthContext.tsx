import React, { createContext, useContext, useState, ReactNode } from "react";

interface User {
	id: string;
	firstname: string;
	lastname: string;
	username: string;
	emailid: string;
	age: string;
	gender: string;
	industry: string;
	profession: string;
}

interface AuthContextType {
	user: User | null;
	isAuthenticated: boolean;
	login: (email: string, password: string) => Promise<boolean>;
	register: (
		userData: Omit<User, "id"> & { password: string }
	) => Promise<boolean>;
	logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
	const [user, setUser] = useState<User | null>(null);

	const login = async (email: string, password: string): Promise<boolean> => {
		try {
			const res = await fetch("http://localhost:5000/api/login", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ emailid: email, password }),
				credentials: "include",
			});
			const data = await res.json();
			if (!res.ok) return false;
			setUser({
				id: data.user_id || data.id,
				firstname: data.firstname,
				lastname: data.lastname,
				username: data.username,
				emailid: data.emailid,
				age: data.age,
				gender: data.gender,
				industry: data.industry,
				profession: data.profession,
			});
			localStorage.setItem("mindcare_current_user", JSON.stringify(data));
			return true;
		} catch (error) {
			return false;
		}
	};

	const register = async (
		userData: Omit<User, "id"> & {
			password: string;
			confirm_password?: string;
		}
	): Promise<boolean> => {
		try {
			const res = await fetch("http://localhost:5000/api/register", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					emailid: userData.emailid,
					username: userData.username,
					firstname: userData.firstname,
					lastname: userData.lastname,
					age: userData.age,
					gender: userData.gender,
					industry: userData.industry,
					profession: userData.profession,
					password: userData.password,
					confirm_password:
						userData.confirm_password || userData.password,
				}),
				credentials: "include",
			});
			const data = await res.json();
			if (!res.ok) return false;
			setUser({
				id: data.user_id || data.id,
				firstname: data.firstname,
				lastname: data.lastname,
				username: data.username,
				emailid: data.emailid,
				age: data.age,
				gender: data.gender,
				industry: data.industry,
				profession: data.profession,
			});
			localStorage.setItem("mindcare_current_user", JSON.stringify(data));
			return true;
		} catch (error) {
			return false;
		}
	};

	const logout = () => {
		setUser(null);
		localStorage.removeItem("mindcare_current_user");
	};

	// Check for existing session on load
	React.useEffect(() => {
		const storedUser = localStorage.getItem("mindcare_current_user");
		if (storedUser) {
			setUser(JSON.parse(storedUser));
		}
	}, []);

	const value = {
		user,
		isAuthenticated: !!user,
		login,
		register,
		logout,
	};

	return (
		<AuthContext.Provider value={value}>{children}</AuthContext.Provider>
	);
}

export function useAuth() {
	const context = useContext(AuthContext);
	if (context === undefined) {
		throw new Error("useAuth must be used within an AuthProvider");
	}
	return context;
}
