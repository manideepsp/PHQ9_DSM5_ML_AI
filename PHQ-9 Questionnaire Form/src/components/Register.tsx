// LinkedIn Industry Taxonomy
const industryProfessionMap: { [key: string]: string[] } = {
	"Information Technology": [
		"Software Engineer",
		"Data Scientist",
		"IT Manager",
		"System Administrator",
		"Web Developer",
		"Mobile Developer",
		"DevOps Engineer",
		"QA Engineer",
		"UI/UX Designer",
		"Product Manager",
		"Business Analyst",
		"Network Engineer",
		"Security Analyst",
		"Database Administrator",
		"Cloud Architect",
		"Technical Support Specialist",
		"IT Consultant",
		"IT Auditor",
		"ERP Specialist",
		"Game Developer",
		"Blockchain Developer",
		"AI/ML Engineer",
		"Other",
	],
	Healthcare: [
		"Doctor",
		"Nurse",
		"Pharmacist",
		"Therapist",
		"Surgeon",
		"Dentist",
		"Radiologist",
		"Medical Laboratory Technician",
		"Physician Assistant",
		"Paramedic",
		"Healthcare Administrator",
		"Physical Therapist",
		"Occupational Therapist",
		"Psychologist",
		"Dietitian",
		"Veterinarian",
		"Optometrist",
		"Speech Pathologist",
		"Chiropractor",
		"Other",
	],
	Education: [
		"Teacher",
		"Professor",
		"Lecturer",
		"School Administrator",
		"Counselor",
		"Librarian",
		"Education Consultant",
		"Instructional Designer",
		"Special Education Teacher",
		"Teaching Assistant",
		"Researcher",
		"Coach",
		"Curriculum Developer",
		"Other",
	],
	Finance: [
		"Accountant",
		"Financial Analyst",
		"Banker",
		"Auditor",
		"Investment Banker",
		"Insurance Agent",
		"Loan Officer",
		"Tax Advisor",
		"Financial Planner",
		"Treasury Analyst",
		"Risk Manager",
		"Compliance Officer",
		"Actuary",
		"Portfolio Manager",
		"Trader",
		"Credit Analyst",
		"Other",
	],
	Manufacturing: [
		"Engineer",
		"Technician",
		"Supervisor",
		"Operator",
		"Production Manager",
		"Quality Control Inspector",
		"Maintenance Engineer",
		"Process Engineer",
		"Supply Chain Manager",
		"Assembler",
		"Machinist",
		"Safety Officer",
		"Manufacturing Planner",
		"Tool and Die Maker",
		"Other",
	],
	Retail: [
		"Salesperson",
		"Store Manager",
		"Cashier",
		"Merchandiser",
		"Inventory Manager",
		"Customer Service Representative",
		"Visual Merchandiser",
		"Retail Buyer",
		"Loss Prevention Specialist",
		"E-commerce Specialist",
		"Department Manager",
		"Other",
	],
	Government: [
		"Civil Servant",
		"Policy Analyst",
		"Administrator",
		"Diplomat",
		"Urban Planner",
		"Public Health Official",
		"Customs Officer",
		"Law Enforcement Officer",
		"Social Worker",
		"Legislative Assistant",
		"Regulatory Affairs Specialist",
		"Other",
	],
	Construction: [
		"Architect",
		"Civil Engineer",
		"Construction Manager",
		"Site Supervisor",
		"Electrician",
		"Plumber",
		"Carpenter",
		"Surveyor",
		"Safety Manager",
		"Estimator",
		"Project Manager",
		"Mason",
		"Roofer",
		"Other",
	],
	Hospitality: [
		"Hotel Manager",
		"Chef",
		"Event Planner",
		"Front Desk Agent",
		"Housekeeping Supervisor",
		"Food and Beverage Manager",
		"Travel Agent",
		"Concierge",
		"Restaurant Manager",
		"Bartender",
		"Catering Manager",
		"Other",
	],
	"Transportation & Logistics": [
		"Logistics Coordinator",
		"Supply Chain Analyst",
		"Truck Driver",
		"Warehouse Manager",
		"Dispatcher",
		"Fleet Manager",
		"Customs Broker",
		"Shipping Clerk",
		"Inventory Analyst",
		"Freight Forwarder",
		"Other",
	],
	"Energy & Utilities": [
		"Energy Analyst",
		"Utility Worker",
		"Electrical Engineer",
		"Power Plant Operator",
		"Environmental Engineer",
		"Renewable Energy Specialist",
		"Field Technician",
		"Safety Inspector",
		"Geologist",
		"Other",
	],
	Legal: [
		"Lawyer",
		"Paralegal",
		"Legal Secretary",
		"Judge",
		"Legal Consultant",
		"Compliance Officer",
		"Court Clerk",
		"Mediator",
		"Legal Analyst",
		"Other",
	],
	"Arts & Entertainment": [
		"Artist",
		"Musician",
		"Actor",
		"Producer",
		"Director",
		"Writer",
		"Graphic Designer",
		"Animator",
		"Photographer",
		"Sound Engineer",
		"Stage Manager",
		"Dancer",
		"Other",
	],
	Other: ["Other"],
};

import React, { useState } from "react";
import {
	Card,
	CardHeader,
	CardTitle,
	CardDescription,
	CardContent,
} from "./ui/card";
import { Button } from "./ui/button";
import {
	UserPlus,
	Mail,
	Lock,
	User,
	Briefcase,
	Hash,
	Calendar,
	Venus,
	Building2,
} from "lucide-react";

export default function Register({ onRegister }: { onRegister: () => void }) {
	const [form, setForm] = useState({
		emailid: "",
		username: "",
		firstname: "",
		lastname: "",
		age: "",
		gender: "",
		industry: "",
		profession: "",
		password: "",
		confirm_password: "",
	});
	const [error, setError] = useState("");
	const [success, setSuccess] = useState("");

	const handleChange = (
		e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
	) => {
		setForm({ ...form, [e.target.name]: e.target.value });
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError("");
		setSuccess("");
		if (!form.emailid.endsWith("@gmail.com")) {
			setError("Email must be a valid @gmail.com address");
			return;
		}
		if (form.password.length < 4) {
			setError("Password must be at least 4 characters");
			return;
		}
		if (form.password !== form.confirm_password) {
			setError("Passwords do not match");
			return;
		}
		try {
			const res = await fetch("http://localhost:5000/api/register", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(form),
			});
			const data = await res.json();
			if (!res.ok) throw new Error(data.error || "Registration failed");
			setSuccess("Registration successful! Please login.");
			onRegister();
		} catch (err: any) {
			setError(err.message);
		}
	};

	return (
		<div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100 py-12">
			<Card className="w-full max-w-md shadow-2xl border-0 bg-white">
				<CardHeader className="bg-blue-600 text-white rounded-t-lg">
					<CardTitle className="text-2xl flex items-center gap-3">
						<UserPlus className="h-6 w-6" /> Register
					</CardTitle>
					<CardDescription className="text-blue-100 text-lg">
						Create your account to access the PHQ-9 assessment.
					</CardDescription>
				</CardHeader>
				<CardContent>
					<form onSubmit={handleSubmit} className="space-y-5 mt-2">
						{error && (
							<div className="mb-4 text-red-600 font-semibold">
								{error}
							</div>
						)}
						{success && (
							<div className="mb-4 text-green-600 font-semibold">
								{success}
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
									name="emailid"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={form.emailid}
									onChange={handleChange}
									required
								/>
							</div>
						</div>
						<div>
							<label className="block mb-1 font-medium">
								Username
							</label>
							<div className="relative">
								<span className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400">
									<Hash className="h-5 w-5" />
								</span>
								<input
									type="text"
									name="username"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={form.username}
									onChange={handleChange}
									required
								/>
							</div>
						</div>
						<div>
							<label className="block mb-1 font-medium">
								First Name
							</label>
							<div className="relative">
								<span className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400">
									<User className="h-5 w-5" />
								</span>
								<input
									type="text"
									name="firstname"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={form.firstname}
									onChange={handleChange}
									required
								/>
							</div>
						</div>
						<div>
							<label className="block mb-1 font-medium">
								Last Name
							</label>
							<div className="relative">
								<span className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400">
									<User className="h-5 w-5" />
								</span>
								<input
									type="text"
									name="lastname"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={form.lastname}
									onChange={handleChange}
									required
								/>
							</div>
						</div>
						<div>
							<label className="block mb-1 font-medium">
								Age
							</label>
							<div className="relative">
								<span className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400">
									<Calendar className="h-5 w-5" />
								</span>
								<input
									type="number"
									name="age"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={form.age}
									onChange={handleChange}
									required
								/>
							</div>
						</div>
						<div>
							<label className="block mb-1 font-medium">
								Gender
							</label>
							<div className="relative">
								<span className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400">
									<Venus className="h-5 w-5" />
								</span>
								<select
									name="gender"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={form.gender}
									onChange={handleChange}
									required
								>
									<option value="">Select Gender</option>
									<option value="Male">Male</option>
									<option value="Female">Female</option>
									<option value="Other">Other</option>
									<option value="Prefer not to say">
										Prefer not to say
									</option>
								</select>
							</div>
						</div>
						<div>
							<label className="block mb-1 font-medium">
								Industry
							</label>
							<div className="relative">
								<span className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400">
									<Building2 className="h-5 w-5" />
								</span>
								<select
									name="industry"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={form.industry}
									onChange={handleChange}
									required
								>
									<option value="">Select Industry</option>
									{Object.keys(industryProfessionMap).map(
										(ind) => (
											<option key={ind} value={ind}>
												{ind}
											</option>
										)
									)}
								</select>
							</div>
						</div>
						<div>
							<label className="block mb-1 font-medium">
								Profession
							</label>
							<div className="relative">
								<span className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400">
									<Briefcase className="h-5 w-5" />
								</span>
								<select
									name="profession"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={form.profession}
									onChange={handleChange}
									required
									disabled={!form.industry}
								>
									<option value="">Select Profession</option>
									{(
										industryProfessionMap[form.industry] ||
										[]
									).map((prof) => (
										<option key={prof} value={prof}>
											{prof}
										</option>
									))}
								</select>
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
									name="password"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={form.password}
									onChange={handleChange}
									required
								/>
							</div>
						</div>
						<div>
							<label className="block mb-1 font-medium">
								Confirm Password
							</label>
							<div className="relative">
								<span className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400">
									<Lock className="h-5 w-5" />
								</span>
								<input
									type="password"
									name="confirm_password"
									className="w-full border p-2 rounded pl-10 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
									value={form.confirm_password}
									onChange={handleChange}
									required
								/>
							</div>
						</div>
						<Button
							type="submit"
							className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg shadow-lg transform transition-all duration-200 hover:scale-105"
						>
							Register
						</Button>
					</form>
				</CardContent>
			</Card>
		</div>
	);
}
