import Header from "../components/common/Header";

import OverviewCards from "../components/modeling/OverviewCards";
import RevenueChart from "../components/modeling/RevenueChart";
import ChannelPerformance from "../components/modeling/ChannelPerformance";
import ProductPerformance from "../components/modeling/ProductPerformance";
import UserRetention from "../components/modeling/UserRetention";
import CustomerSegmentation from "../components/modeling/CustomerSegmentation";
import AIPoweredInsights from "../components/modeling/AIPoweredInsights";

const ModelingPage = () => {
	return (
		<div className='flex-1 overflow-auto relative z-10 bg-gray-900'>
			<Header title={"Analytics Dashboard"} />

			<main className='max-w-7xl mx-auto py-6 px-4 lg:px-8'>
				<OverviewCards />
				<RevenueChart />

				<div className='grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'>
					<ChannelPerformance />
					<ProductPerformance />
					<UserRetention />
					<CustomerSegmentation />
				</div>

				<AIPoweredInsights />
			</main>
		</div>
	);
};
export default ModelingPage;
