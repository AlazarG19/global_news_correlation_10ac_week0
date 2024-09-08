import { Route, Routes } from "react-router-dom";

import Sidebar from "./components/common/Sidebar";
import 'bootstrap/dist/css/bootstrap.min.css';
import OverviewPage from "./pages/OverviewPage";
import QuantitativeWebsitePage from "./pages/QuantitativeWebsitePage";
import QuantitativeCountryPage from "./pages/QuantitativeCountryPage";

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

			</Routes>
		</div>
	);
}

export default App;
