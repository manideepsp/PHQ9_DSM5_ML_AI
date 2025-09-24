import React, { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "./ui/card";
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "./ui/select";
import { useAuth } from "../contexts/AuthContext";
import {
	UserPlus,
	Eye,
	EyeOff,
	User,
	Mail,
	Lock,
	Calendar,
	Briefcase,
	Shield,
} from "lucide-react";

interface RegistrationFormProps {
	onSwitchToLogin: () => void;
}

export function RegistrationForm({ onSwitchToLogin }: RegistrationFormProps) {
	const [formData, setFormData] = useState({
		name: "",
		username: "",
		email: "",
		password: "",
		confirmPassword: "",
		age: "",
		gender: "",
		industry: "",
		profession: "",
		dateOfBirth: "",
	});
	const [showPassword, setShowPassword] = useState(false);
	const [showConfirmPassword, setShowConfirmPassword] = useState(false);
	const [error, setError] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const { register } = useAuth();

	const handleInputChange = (field: string, value: string) => {
		setFormData((prev) => ({
			...prev,
			[field]: value,
		}));
	};

	const validateForm = () => {
		if (
			!formData.name ||
			!formData.username ||
			!formData.email ||
			!formData.password ||
			!formData.age ||
			!formData.gender ||
			!formData.industry ||
			!formData.profession ||
			!formData.dateOfBirth
		) {
			return "Please fill in all fields";
		}

		if (formData.password !== formData.confirmPassword) {
			return "Passwords do not match";
		}

		if (formData.password.length < 6) {
			return "Password must be at least 6 characters";
		}

		const age = parseInt(formData.age);
		if (isNaN(age) || age < 13 || age > 120) {
			return "Please enter a valid age between 13 and 120";
		}

		const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		if (!emailRegex.test(formData.email)) {
			return "Please enter a valid email address";
		}

		return null;
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError("");

		const validationError = validateForm();
		if (validationError) {
			setError(validationError);
			return;
		}

		setIsLoading(true);

		// Split name into firstname and lastname
		const [firstname, ...lastnameArr] = formData.name.trim().split(" ");
		const lastname = lastnameArr.join(" ") || "";
		const success = await register({
			firstname,
			lastname,
			username: formData.username,
			emailid: formData.email,
			password: formData.password,
			age: formData.age,
			gender: formData.gender,
			industry: formData.industry,
			profession: formData.profession,
		});

		if (!success) {
			setError("An account with this email already exists");
		}

		setIsLoading(false);
	};

	const industries = [
		"Technology, Information and Internet",
		"Financial Services",
		"Healthcare",
		"Education",
		"Manufacturing",
		"Retail",
		"Construction",
		"Real Estate",
		"Transportation, Logistics, Supply Chain and Storage",
		"Government Administration",
		"Non-profit Organization Management",
		"Entertainment Providers",
		"Food and Beverages",
		"Telecommunications",
		"Oil, Gas, and Mining",
		"Automotive",
		"Media and Communications",
		"Professional Services",
		"Consumer Services",
		"Hospitality",
		"Agriculture",
		"Legal Services",
		"Utilities",
		"Aviation and Aerospace",
		"Maritime",
		"Defense and Space",
		"Architecture and Planning",
		"Design",
		"Research Services",
		"Environmental Services",
		"Other",
	];

	const professions = [
		"Software Engineering",
		"Data Science",
		"Product Management",
		"Marketing",
		"Sales",
		"Human Resources",
		"Finance",
		"Operations",
		"Customer Success",
		"Design",
		"Research",
		"Consulting",
		"Business Development",
		"Strategy",
		"Legal",
		"Healthcare",
		"Education",
		"Engineering",
		"Management",
		"Administration",
		"Writing",
		"Public Relations",
		"Quality Assurance",
		"Information Technology",
		"Project Management",
		"Business Analysis",
		"Customer Service",
		"Supply Chain",
		"Manufacturing",
		"Construction",
		"Real Estate",
		"Insurance",
		"Banking",
		"Accounting",
		"Recruitment",
		"Training",
		"Procurement",
		"Risk Management",
		"Compliance",
		"Security",
		"Architecture",
		"Planning",
		"Student",
		"Retired",
		"Other",
	];

	return (
		<div className="min-h-screen bg-blue-50 flex items-center justify-center p-6">
			<Card className="w-full max-w-2xl shadow-2xl border-0 bg-white">
				<CardHeader className="bg-blue-600 text-white rounded-t-lg text-center">
					<div className="flex justify-center mb-3">
						<div className="bg-blue-500 p-3 rounded-full">
							<UserPlus className="h-8 w-8 text-white" />
						</div>
					</div>
					<CardTitle className="text-2xl">
						Create Your Account
					</CardTitle>
					<CardDescription className="text-blue-100">
						Join MindCare to access mental health assessments
					</CardDescription>
				</CardHeader>

				<CardContent className="p-8">
					<form onSubmit={handleSubmit} className="space-y-6">
						{error && (
							<div className="bg-red-50 border border-red-200 p-4 rounded-lg">
								<p className="text-red-700 text-sm">{error}</p>
							</div>
						)}

						<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
							<div className="space-y-2">
								<Label
									htmlFor="gender"
									className="text-gray-700"
								>
									Gender
								</Label>
								<div className="relative">
									<Shield className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
									<select
										id="gender"
										value={formData.gender}
										onChange={(e) =>
											handleInputChange(
												"gender",
												e.target.value
											)
										}
										className="pl-10 border-gray-300 focus:border-blue-500 focus:ring-blue-500 rounded w-full h-10"
										required
									>
										<option value="">Select gender</option>
										<option value="Male">Male</option>
										<option value="Female">Female</option>
										<option value="Other">Other</option>
										<option value="Prefer not to say">
											Prefer not to say
										</option>
									</select>
								</div>
							</div>
							<div className="space-y-2">
								<Label htmlFor="name" className="text-gray-700">
									Full Name
								</Label>
								<div className="relative">
									<User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
									<Input
										id="name"
										type="text"
										value={formData.name}
										onChange={(e) =>
											handleInputChange(
												"name",
												e.target.value
											)
										}
										className="pl-10 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
										placeholder="Enter your full name"
										required
									/>
								</div>
							</div>

							<div className="space-y-2">
								<Label
									htmlFor="username"
									className="text-gray-700"
								>
									Username
								</Label>
								<div className="relative">
									<User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
									<Input
										id="username"
										type="text"
										value={formData.username}
										onChange={(e) =>
											handleInputChange(
												"username",
												e.target.value
											)
										}
										className="pl-10 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
										placeholder="Choose a username"
										required
									/>
								</div>
							</div>
						</div>

						<div className="space-y-2">
							<Label htmlFor="email" className="text-gray-700">
								Email Address
							</Label>
							<div className="relative">
								<Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
								<Input
									id="email"
									type="email"
									value={formData.email}
									onChange={(e) =>
										handleInputChange(
											"email",
											e.target.value
										)
									}
									className="pl-10 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
									placeholder="Enter your email"
									required
								/>
							</div>
						</div>

						<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
							<div className="space-y-2">
								<Label
									htmlFor="password"
									className="text-gray-700"
								>
									Password
								</Label>
								<div className="relative">
									<Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
									<Input
										id="password"
										type={
											showPassword ? "text" : "password"
										}
										value={formData.password}
										onChange={(e) =>
											handleInputChange(
												"password",
												e.target.value
											)
										}
										className="pl-10 pr-10 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
										placeholder="Create a password"
										required
									/>
									<Button
										type="button"
										variant="ghost"
										size="sm"
										className="absolute right-1 top-1/2 transform -translate-y-1/2 h-8 w-8 p-0 hover:bg-gray-100"
										onClick={() =>
											setShowPassword(!showPassword)
										}
									>
										{showPassword ? (
											<EyeOff className="h-4 w-4" />
										) : (
											<Eye className="h-4 w-4" />
										)}
									</Button>
								</div>
							</div>

							<div className="space-y-2">
								<Label
									htmlFor="confirmPassword"
									className="text-gray-700"
								>
									Confirm Password
								</Label>
								<div className="relative">
									<Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
									<Input
										id="confirmPassword"
										type={
											showConfirmPassword
												? "text"
												: "password"
										}
										value={formData.confirmPassword}
										onChange={(e) =>
											handleInputChange(
												"confirmPassword",
												e.target.value
											)
										}
										className="pl-10 pr-10 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
										placeholder="Confirm your password"
										required
									/>
									<Button
										type="button"
										variant="ghost"
										size="sm"
										className="absolute right-1 top-1/2 transform -translate-y-1/2 h-8 w-8 p-0 hover:bg-gray-100"
										onClick={() =>
											setShowConfirmPassword(
												!showConfirmPassword
											)
										}
									>
										{showConfirmPassword ? (
											<EyeOff className="h-4 w-4" />
										) : (
											<Eye className="h-4 w-4" />
										)}
									</Button>
								</div>
							</div>
						</div>

						<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
							<div className="space-y-2">
								<Label htmlFor="age" className="text-gray-700">
									Age
								</Label>
								<Input
									id="age"
									type="number"
									value={formData.age}
									onChange={(e) =>
										handleInputChange("age", e.target.value)
									}
									className="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
									placeholder="Enter your age"
									min="13"
									max="120"
									required
								/>
							</div>

							<div className="space-y-2">
								<Label
									htmlFor="dateOfBirth"
									className="text-gray-700"
								>
									Date of Birth
								</Label>
								<div className="relative">
									<Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
									<Input
										id="dateOfBirth"
										type="date"
										value={formData.dateOfBirth}
										onChange={(e) =>
											handleInputChange(
												"dateOfBirth",
												e.target.value
											)
										}
										className="pl-10 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
										required
									/>
								</div>
							</div>
						</div>

						<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
							<div className="space-y-2">
								<Label
									htmlFor="industry"
									className="text-gray-700"
								>
									Industry
								</Label>
								<div className="relative">
									<Briefcase className="absolute left-3 top-3 h-5 w-5 text-gray-400 z-10" />
									<Select
										onValueChange={(value) =>
											handleInputChange("industry", value)
										}
										required
									>
										<SelectTrigger className="pl-10 border-gray-300 focus:border-blue-500 focus:ring-blue-500">
											<SelectValue placeholder="Select your industry" />
										</SelectTrigger>
										<SelectContent>
											{industries.map((industry) => (
												<SelectItem
													key={industry}
													value={industry}
												>
													{industry}
												</SelectItem>
											))}
										</SelectContent>
									</Select>
								</div>
							</div>

							<div className="space-y-2">
								<Label
									htmlFor="profession"
									className="text-gray-700"
								>
									Profession
								</Label>
								<div className="relative">
									<Shield className="absolute left-3 top-3 h-5 w-5 text-gray-400 z-10" />
									<Select
										onValueChange={(value) =>
											handleInputChange(
												"profession",
												value
											)
										}
										required
									>
										<SelectTrigger className="pl-10 border-gray-300 focus:border-blue-500 focus:ring-blue-500">
											<SelectValue placeholder="Select your profession" />
										</SelectTrigger>
										<SelectContent>
											{professions.map((profession) => (
												<SelectItem
													key={profession}
													value={profession}
												>
													{profession}
												</SelectItem>
											))}
										</SelectContent>
									</Select>
								</div>
							</div>
						</div>

						<Button
							type="submit"
							disabled={isLoading}
							className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 shadow-lg transform transition-all duration-200 hover:scale-105"
						>
							{isLoading
								? "Creating Account..."
								: "Create Account"}
						</Button>
					</form>

					<div className="mt-8 text-center">
						<p className="text-gray-600">
							Already have an account?{" "}
							<button
								type="button"
								onClick={onSwitchToLogin}
								className="text-blue-600 hover:text-blue-700 underline transition-colors"
							>
								Sign in here
							</button>
						</p>
					</div>
				</CardContent>
			</Card>
		</div>
	);
}
