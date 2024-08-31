import { motion } from "framer-motion";

import Header from "../components/common/Header";
import StatCard from "../components/common/StatCard";
import { CreditCard, DollarSign, ShoppingCart, TrendingUp } from "lucide-react";
import SalesOverviewChart from "../components/titlesentiment/SalesOverviewChart";
import SalesByCategoryChart from "../components/titlesentiment/SalesByCategoryChart";
import DailySalesTrend from "../components/titlesentiment/DailySalesTrend";
import { useEffect, useState } from "react";
import TitleSentimentDistributionChart from "../components/overview/TitleSentimentDistributionChart";

const salesStats = {
	totalRevenue: "$1,234,567",
	averageOrderValue: "$78.90",
	conversionRate: "3.45%",
	salesGrowth: "12.3%",
};

const TitleSentimentPage = () => {
	const [overviewData, setOverviewData] = useState({})
	let urls = [
		`${import.meta.env.VITE_BACKEND_URL}/gettitlesentimentcomposition`]
	async function fetchAndCombineData(urls) {
		try {
			// Use Promise.all to send requests to all URLs simultaneously
			const responses = await Promise.all(urls.map(url => fetch(url)));

			// Wait for all responses to resolve to JSON
			const data = await Promise.all(responses.map(response => response.json()));

			// Combine the data into a dictionary with the URL as the key
			const combinedData = urls.reduce((acc, url, index) => {
				const lastSubPath = url.split('/').filter(part => part).pop();
				acc[lastSubPath] = data[index];
				return acc;
			}, {});
			console.log(combinedData)
			return combinedData;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}


	// Usage
	useEffect(() => {
		fetchAndCombineData(urls)
			.then(combinedData => {
				setOverviewData(combinedData)
			});

	}, [])

	return (
		<div className='flex-1 overflow-auto relative z-10'>
			<Header title='Sales Dashboard' />

			<main className='max-w-7xl mx-auto py-6 px-4 lg:px-8'>
				{/* SALES STATS */}


				<SalesOverviewChart />

				<div className='grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'>
					<TitleSentimentDistributionChart titlesentimentdata={Object.keys(overviewData).length != 0 ? overviewData.gettitlesentimentcomposition : []} />

					<DailySalesTrend />
				</div>
			</main>
		</div>
	);
};
export default TitleSentimentPage;
