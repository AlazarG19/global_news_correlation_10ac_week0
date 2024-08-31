import { Route, Routes } from "react-router-dom";

import Sidebar from "./components/common/Sidebar";

import OverviewPage from "./pages/OverviewPage";
import QuantitativeWebsitePage from "./pages/QuantitativeWebsitePage";
import QuantitativeCountryPage from "./pages/QuantitativeCountryPage";
import TitleSentimentPage from "./pages/TitleSentimentPage";
import OrdersPage from "./pages/OrdersPage";
import ModelingPage from "./pages/ModelingPage";
import SettingsPage from "./pages/SettingsPage";

function App() {
	return (
		<div className='flex h-screen bg-gray-900 text-gray-100 overflow-hidden'>
			{/* BG */}
			<div className='fixed inset-0 z-0'>
				<div className='absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 opacity-80' />
				<div className='absolute inset-0 backdrop-blur-sm' />
			</div>

			<Sidebar />
			<Routes>
				<Route path='/' element={<OverviewPage />} />
				<Route path='/quantitativewebsite' element={<QuantitativeWebsitePage />} />
				<Route path='/quantitativecountry' element={<QuantitativeCountryPage />} />
				{/* <Route path='/titlesentiment' element={<TitleSentimentPage />} />
				<Route path='/metadata' element={<OrdersPage />} />
				<Route path='/modeling' element={<ModelingPage />} />
				<Route path='/events' element={<SettingsPage />} /> */}
			</Routes>
		</div>
	);
}

export default App;
