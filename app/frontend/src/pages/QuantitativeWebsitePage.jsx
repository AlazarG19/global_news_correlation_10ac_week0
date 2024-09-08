import { motion } from "framer-motion";

import Header from "../components/common/Header";
import WebsiteLeastVisitors from "../components/quantiativewebsite/WebsiteLeastVisitors";
import WebsiteMostVisitors from "../components/quantiativewebsite/WebsiteMostVisitors";
import CountryLeastArticle from "../components/quantiativewebsite/CountryLeastArticle";
import CountryMostArticle from "../components/quantiativewebsite/CountryMostArticle";
import RankWebsiteTable from "../components/quantiativewebsite/RankWebsiteTable";
import { useEffect, useState } from "react";
import Loading from "../components/Loading";

const QuantitativeWebsitePage = () => {
	const [overviewData, setOverviewData] = useState({})
	const [loading, setLoading] = useState(true)
	let urls = [
		`${import.meta.env.VITE_BACKEND_URL}/getcountryarticletopcountdata`,
		`${import.meta.env.VITE_BACKEND_URL}/getcountryarticlebottomcountdata`,
		`${import.meta.env.VITE_BACKEND_URL}/getwebsitevisitortopcountdata`,
		`${import.meta.env.VITE_BACKEND_URL}/getwebsitevisitorbottomcountdata`,
		`${import.meta.env.VITE_BACKEND_URL}/getsortedtraffic`,
	];
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
			<Header title='Products' />

			<main className='max-w-7xl mx-auto py-6 px-4 lg:px-8'>

				{/* CHARTS */}
				<div className='grid grid-col-1 lg:grid-cols-2 gap-8'>

					{loading ? <Loading /> : <CountryMostArticle articledata={Object.keys(overviewData).length != 0 ? overviewData.getcountryarticletopcountdata["data"] : []} />}
					{loading ? <Loading /> :
						<CountryLeastArticle articledata={Object.keys(overviewData).length != 0 ? overviewData.getcountryarticlebottomcountdata["data"] : []} />
					}
					{loading ? <Loading /> :
						<WebsiteMostVisitors visitordata={Object.keys(overviewData).length != 0 ? overviewData.getwebsitevisitortopcountdata : []} />
					}
					{loading ? <Loading /> :
						<WebsiteLeastVisitors visitordata={Object.keys(overviewData).length != 0 ? overviewData.getwebsitevisitorbottomcountdata : []} />
					}
					{loading ? <Loading /> :
						<div className='lg:col-span-2'>
							<RankWebsiteTable trafficdata={Object.keys(overviewData).length != 0 ? overviewData.getsortedtraffic : []} />
						</div>
					}

				</div>
			</main>
		</div>
	);
};
export default QuantitativeWebsitePage;
