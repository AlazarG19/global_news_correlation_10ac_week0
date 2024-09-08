import { BarChart2, ShoppingBag, Users, Zap } from "lucide-react";
import { motion } from "framer-motion";

import Header from "../components/common/Header";
import StatCard from "../components/common/StatCard";
import SalesOverviewChart from "../components/overview/SalesOverviewChart";
import CategoryDistributionChart from "../components/overview/CategoryDistributionChart";
import SalesChannelChart from "../components/overview/SalesChannelChart";
import RatingsTable from "../components/quantiativewebsite/RatingTable";
import TrafficsTable from "../components/quantiativewebsite/TrafficTable";
import TitleSentimentDistributionChart from "../components/overview/TitleSentimentDistributionChart";
import CountriesArticleChartChart from "../components/overview/CountriesArticleChart";
import { useEffect, useState } from "react";
import Loading from "../components/Loading";

const OverviewPage = () => {
	const [overviewData, setOverviewData] = useState({})
	const [loading, setLoading] = useState({})
	let urls = [
		`${import.meta.env.VITE_BACKEND_URL}/getoverviewcardvalues`,
		`${import.meta.env.VITE_BACKEND_URL}/getcountryarticletopcountdata`,
		`${import.meta.env.VITE_BACKEND_URL}/gettitlesentimentcomposition`,
		`${import.meta.env.VITE_BACKEND_URL}/getrating`
	];
	async function fetchAndCombineData(urls) {
		try {
			// Use Promise.all to send requests to all URLs simultaneously
			const responses = await Promise.all(urls.map(url => fetch(url, { mode: 'cors' })));

			// Wait for all responses to resolve to JSON
			const data = await Promise.all(responses.map(response => response.json()));

			// Combine the data into a dictionary with the URL as the key
			const combinedData = urls.reduce((acc, url, index) => {
				const lastSubPath = url.split('/').filter(part => part).pop();
				acc[lastSubPath] = data[index];
				return acc;
			}, {});
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
				setLoading(false)
			});

	}, [])

	return (
		<div className='flex-1 overflow-auto relative z-10'>
			<Header title='Overview' />

			<main className='max-w-7xl mx-auto py-6 px-4 lg:px-8'>
				{/* STATS */}
				<motion.div
					className='grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8'
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 1 }}
				>
					{loading ? <Loading /> : <StatCard name='Number of Domains' icon={Zap} value={Object.keys(overviewData).length != 0 ? overviewData["getoverviewcardvalues"]["domains_location"] : 0} color='#6366F1' />}
					{loading ? <Loading /> : <StatCard name='Number of Rating Data' icon={Users} value={Object.keys(overviewData).length != 0 ? overviewData["getoverviewcardvalues"]["rating"] : 0} color='#8B5CF6' />}
					{loading ? <Loading /> : <StatCard name='Number of Traffic Data' icon={ShoppingBag} value={Object.keys(overviewData).length != 0 ? overviewData["getoverviewcardvalues"]["traffic"] : 0} color='#EC4899' />}
					{loading ? <Loading /> : <StatCard name='Number of Newly Created Features' icon={BarChart2} value={Object.keys(overviewData).length != 0 ? overviewData["getoverviewcardvalues"]["new_features"] : 0} color='#10B981' />}




				</motion.div>

				{/* CHARTS */}

				<div className='grid grid-cols-1 lg:grid-cols-2  gap-8'>
					{/* <SalesOverviewChart /> */}
					{loading ? <Loading /> :
						<TitleSentimentDistributionChart titlesentimentdata={Object.keys(overviewData).length != 0 ? overviewData.gettitlesentimentcomposition : []} />
					}
					{loading ? <Loading /> :
						<CountriesArticleChartChart articledata={Object.keys(overviewData).length != 0 ? overviewData.getcountryarticletopcountdata["data"] : []} />
					}
					{loading ? <Loading /> :
						<div className='lg:col-span-2'>
							<RatingsTable ratingdata={Object.keys(overviewData).length != 0 ? overviewData.getrating : []} />

						</div>
					}
				</div>
			</main>
		</div>
	);
};
export default OverviewPage;
