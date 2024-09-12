import { BarChart4, UserCheck, UserPlus, UsersIcon, UserX } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";


import CountryMostMedia from "../components/settings/CountryMostMedia";
import CountryLeastMedia from "../components/settings/CountryLeastMedia";

import { Link } from "react-router-dom";
import CountryMostMention from "../components/settings/CountryMostMention";
import CountryLeastMention from "../components/settings/CountryLeastMention";
import RegionMostMention from "../components/settings/RegionMostMention";
import RegionLeastMention from "../components/settings/RegionLeastMention";
import { useEffect, useState } from "react";
import Loading from "../components/Loading";

const QuantitativeCountryPage = () => {
	const [option, setOption] = useState("category")
	const [loading, setLoading] = useState(true)

	const [overviewData, setOverviewData] = useState({})
	let urls = [
		`${import.meta.env.VITE_BACKEND_URL}/getcountrymediatopcountdata`,
		`${import.meta.env.VITE_BACKEND_URL}/getcountrymediabottomcountdata`,
		`${import.meta.env.VITE_BACKEND_URL}/getcontentcountrymentiontopcountdata`,
		`${import.meta.env.VITE_BACKEND_URL}/getcontentcountrymentionbottomcountdata`,
		`${import.meta.env.VITE_BACKEND_URL}/getcontentregionmentioncountdata`,
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
	useEffect(() => {
		fetchAndCombineData(urls)
			.then(combinedData => {
				setOverviewData(combinedData)
				setLoading(false)
			});

	}, [option])
	return (
		<div className='flex-1 overflow-auto relative z-10'>

			<main className='max-w-7xl mx-auto py-6 px-4 lg:px-8'>


				{/* USER CHARTS */}
				<div className='grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8'>
					{/* <Dropdown options={options} onChange={this._onSelect} value={defaultOption} placeholder="Select an option" />;<CountryMostArtic /> */}
					<div className='lg:col-span-2'>
						{loading ? <Loading /> :

							<CountryMostMedia mediadata={Object.keys(overviewData).length != 0 ? overviewData.getcountrymediatopcountdata["data"] : []} />
						}
					</div>
					<div className='lg:col-span-2'>
						<div className="flex justify-between">

							<div>
								<button onClick={() => { setOption("category") }} className={option == "category" ? 'mx-5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-200 w-full sm:w-auto' : 'mx-5 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition duration-200 w-full sm:w-auto'}>
									Based on Category
								</button>
								<button onClick={() => { setOption("content") }} className={option == "content" ? 'mx-5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-200 w-full sm:w-auto' : 'mx-5 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition duration-200 w-full sm:w-auto'}>
									Based on Content
								</button>

							</div>
							<div style={{ fontSize: "18px", fontWeight: "bold" }}>
								Based On {option.toUpperCase()}
							</div>
						</div>
					</div>
					{loading ? <Loading /> :

						<CountryMostMention mentiondata={Object.keys(overviewData).length != 0 ? overviewData.getcontentcountrymentiontopcountdata : []} />
					}
					{loading ? <Loading /> :

						<CountryLeastMention mentiondata={Object.keys(overviewData).length != 0 ? overviewData.getcontentcountrymentionbottomcountdata : []} />
					}
					<div className='lg:col-span-2'>
						<h2>Region</h2>
					</div>
					{loading ? <Loading /> :

						<RegionMostMention regiondata={Object.keys(overviewData).length != 0 ? overviewData.getcontentregionmentioncountdata["data"] : []} />
					}

				</div>
			</main>
		</div>
	);
};
export default QuantitativeCountryPage;
