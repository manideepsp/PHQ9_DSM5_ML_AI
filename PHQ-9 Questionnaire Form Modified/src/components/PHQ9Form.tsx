import React, { useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { Button } from "./ui/button";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "./ui/card";
import { Progress } from "./ui/progress";
import { CheckCircle, AlertTriangle, Info } from "lucide-react";

interface PHQ9Responses {
	[key: number]: number;
}

const phq9Questions = [
	"Little interest or pleasure in doing things",
	"Feeling down, depressed, or hopeless",
	"Trouble falling or staying asleep, or sleeping too much",
	"Feeling tired or having little energy",
	"Poor appetite or overeating",
	"Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
	"Trouble concentrating on things, such as reading the newspaper or watching television",
	"Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
	"Thoughts that you would be better off dead or of hurting yourself in some way",
];

const responseOptions = [
	{
		value: 0,
		label: "Not at all",
		color: "bg-green-500",
		hoverColor: "hover:bg-green-600",
	},
	{
		value: 1,
		label: "Several days",
		color: "bg-yellow-500",
		hoverColor: "hover:bg-yellow-600",
	},
	{
		value: 2,
		label: "More than half the days",
		color: "bg-orange-500",
		hoverColor: "hover:bg-orange-600",
	},
	{
		value: 3,
		label: "Nearly every day",
		color: "bg-red-500",
		hoverColor: "hover:bg-red-600",
	},
];

const PHQ9Form: React.FC = () => {
	const [responses, setResponses] = useState<PHQ9Responses>({});
	const [isSubmitted, setIsSubmitted] = useState(false);
	const { user } = useAuth();

	const handleResponseChange = (questionIndex: number, value: number) => {
		setResponses((prev) => ({
			...prev,
			[questionIndex]: value,
		}));
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		// Check if all questions are answered
		const allAnswered = phq9Questions.every((_, index) =>
			responses.hasOwnProperty(index)
		);
		if (!allAnswered) {
			alert("Please answer all questions before submitting.");
			return;
		}
		// Calculate total score
		const totalScore = Object.values(responses).reduce(
			(sum, score) => sum + score,
			0
		);
		if (!user) {
			alert("You must be logged in to submit the assessment.");
			return;
		}
		try {
			const res = await fetch("http://localhost:5000/api/phq9", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					user_id: user.id,
					responses,
					totalScore,
				}),
				credentials: "include",
			});
			if (!res.ok) {
				const data = await res.json();
				throw new Error(data.error || "Failed to submit assessment");
			}
			setIsSubmitted(true);
			// Provide feedback based on score
			let severity = "";
			if (totalScore >= 0 && totalScore <= 4)
				severity = "Minimal depression";
			else if (totalScore >= 5 && totalScore <= 9)
				severity = "Mild depression";
			else if (totalScore >= 10 && totalScore <= 14)
				severity = "Moderate depression";
			else if (totalScore >= 15 && totalScore <= 19)
				severity = "Moderately severe depression";
			else if (totalScore >= 20) severity = "Severe depression";
			alert(
				`Form submitted successfully!\nTotal Score: ${totalScore}\nSeverity: ${severity}\n\nNote: This is for screening purposes only. Please consult a healthcare professional for proper evaluation.`
			);
		} catch (err: any) {
			alert(err.message || "Failed to submit assessment.");
		}
	};

	const resetForm = () => {
		setResponses({});
		setIsSubmitted(false);
	};

	const progress =
		(Object.keys(responses).length / phq9Questions.length) * 100;

	return (
		<div className="max-w-4xl mx-auto p-6">
			<Card className="shadow-2xl border-0 bg-white">
				<CardHeader className="bg-blue-600 text-white rounded-t-lg">
					<CardTitle className="text-2xl flex items-center gap-3">
						<div className="bg-white/20 p-2 rounded-full">
							<Info className="h-6 w-6" />
						</div>
						PHQ-9 Depression Screening Questionnaire
					</CardTitle>
					<CardDescription className="text-blue-100 text-lg">
						Over the last 2 weeks, how often have you been bothered
						by any of the following problems?
					</CardDescription>
					<div className="mt-4">
						<div className="flex justify-between items-center mb-2">
							<span className="text-sm text-blue-100">
								Progress
							</span>
							<span className="text-sm text-blue-100">
								{Object.keys(responses).length}/
								{phq9Questions.length}
							</span>
						</div>
						<Progress value={progress} className="bg-blue-500" />
					</div>
				</CardHeader>
				<CardContent>
					<form onSubmit={handleSubmit} className="space-y-8">
						{phq9Questions.map((question, questionIndex) => (
							<div key={questionIndex} className="space-y-4">
								<div className="space-y-4">
									<div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
										<h3 className="leading-relaxed text-gray-800 font-medium">
											{questionIndex + 1}. {question}
										</h3>
									</div>
									<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
										{responseOptions.map((option) => (
											<Button
												key={option.value}
												type="button"
												variant="ghost"
												className={`h-auto p-4 text-left justify-start whitespace-normal border-2 transition-all duration-300 ${
													responses[questionIndex] ===
													option.value
														? `${option.color} text-white border-transparent shadow-lg transform scale-105`
														: "bg-white hover:bg-gray-50 border-gray-200 hover:border-blue-300 hover:shadow-md text-gray-700"
												}`}
												onClick={() =>
													handleResponseChange(
														questionIndex,
														option.value
													)
												}
												disabled={isSubmitted}
											>
												<div className="flex items-center justify-center w-full">
													<span className="font-medium">
														{option.label}
													</span>
												</div>
											</Button>
										))}
									</div>
								</div>
								{questionIndex < phq9Questions.length - 1 && (
									<div className="flex justify-center my-6">
										<div className="w-24 h-1 bg-blue-300 rounded-full"></div>
									</div>
								)}
							</div>
						))}

						<div className="flex gap-4 pt-8 border-t border-blue-200">
							<Button
								type="submit"
								disabled={isSubmitted}
								className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-lg transform transition-all duration-200 hover:scale-105"
							>
								{isSubmitted ? (
									<div className="flex items-center gap-2">
										<CheckCircle className="h-5 w-5" />
										Submitted Successfully
									</div>
								) : (
									"Submit PHQ-9 Assessment"
								)}
							</Button>

							{isSubmitted && (
								<Button
									type="button"
									variant="outline"
									onClick={resetForm}
									className="px-8 py-3 border-2 border-blue-300 text-blue-600 hover:bg-blue-50 font-semibold rounded-lg transition-all duration-200 hover:scale-105"
								>
									Take Assessment Again
								</Button>
							)}
						</div>

						<div className="bg-yellow-50 border border-yellow-200 p-6 rounded-lg shadow-md">
							<div className="flex items-start gap-3">
								<AlertTriangle className="h-6 w-6 text-yellow-600 mt-1 flex-shrink-0" />
								<div className="text-sm text-yellow-800">
									<p className="mb-2 font-semibold">
										Important Disclaimer:
									</p>
									<p className="mb-2">
										This questionnaire is for screening
										purposes only and is not a diagnostic
										tool. Results should be discussed with a
										qualified healthcare professional.
									</p>
									<p className="font-semibold text-red-700">
										If you are experiencing thoughts of
										self-harm, please seek immediate
										professional help or contact a crisis
										helpline.
									</p>
								</div>
							</div>
						</div>
					</form>
				</CardContent>
			</Card>
		</div>
	);
};

export default PHQ9Form;
