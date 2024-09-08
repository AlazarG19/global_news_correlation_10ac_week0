import { motion } from "framer-motion";
import { Edit, Search, Trash2 } from "lucide-react";
import { useMemo, useState } from "react";
import { useTable, usePagination } from "react-table";
import "./RatingTable.css"
const RATING_DATA = [
	{ id: 1, name: "Wireless Earbuds", category: "Electronics", price: 59.99, stock: 143, sales: 1200 },
	{ id: 2, name: "Leather Wallet", category: "Accessories", price: 39.99, stock: 89, sales: 800 },
	{ id: 3, name: "Smart Watch", category: "Electronics", price: 199.99, stock: 56, sales: 650 },
	{ id: 4, name: "Yoga Mat", category: "Fitness", price: 29.99, stock: 210, sales: 950 },
	{ id: 5, name: "Coffee Maker", category: "Home", price: 79.99, stock: 78, sales: 720 },
];
const RATING_COLUMNS = [
	{
		Header: "Id",
		accessor: "article_id"
	},
	{
		Header: "Source Name",
		accessor: "source_name"
	},
	{
		Header: "Domain",
		accessor: "domain"
	},
	{
		Header: "Mentioned Countries",
		accessor: "mentioned_countries"
	},

	{
		Header: "Title",
		accessor: "title_sentiment"
	}
];
const INITIAL_STATE = {
	pageSize: 10,
	pageIndex: 0
};

const RatingsTable = ({ ratingdata }) => {
	const data = ratingdata
	const columns = RATING_COLUMNS;
	const initialState = INITIAL_STATE;
	const [searchTerm, setSearchTerm] = useState("");

	const {
		getTableProps,
		getTableBodyProps,
		headerGroups,
		prepareRow,
		page,
		canPreviousPage,
		canNextPage,
		pageOptions,
		pageCount,
		gotoPage,
		nextPage,
		previousPage,
		setPageSize,
		state: { pageIndex, pageSize }
	} = useTable(
		{
			columns: columns || [],  // Ensure columns is not undefined
			data: data || [],
			initialState
		},
		usePagination // highlight-line
	);

	return (
		ratingdata.length != 0 ?
			<motion.div
				className='bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700 mb-8'
				initial={{ opacity: 0, y: 20 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{ delay: 0.2 }}
			>
				<div className='flex justify-between items-center mb-6'>
					<h2 className='text-xl font-semibold text-gray-100'>Rating List</h2>
					<div className='relative'>
						<input
							type='text'
							placeholder='Search ratings...'
							className='bg-gray-700 text-white placeholder-gray-400 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
							onChange={() => { }}
							value={searchTerm}
						/>
						<Search className='absolute left-3 top-2.5 text-gray-400' size={18} />
					</div>
				</div>

				<div className='overflow-x-auto'>
					<table className='min-w-full divide-y divide-gray-700'  {...getTableProps()}>
						<thead>
							{headerGroups.map((headerGroup) => (
								<tr {...headerGroup.getHeaderGroupProps()}>
									{headerGroup.headers.map((column) => (
										<th className='px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider' {...column.getHeaderProps()}>{column.render("Header")}</th>
									))}
								</tr>
							))}
							<tr>
							</tr>
						</thead>

						<tbody {...getTableBodyProps()} className='divide-y divide-gray-700'>
							{page.map((row) => {
								prepareRow(row);
								return (
									<motion.tr
										key={row.id}
										initial={{ opacity: 0 }}
										animate={{ opacity: 1 }}
										transition={{ duration: 0.3 }}
									>
										{row.cells.map((cell) => {
											return (
												<td
													className='px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-100 gap-2 items-center'
													{...cell.getCellProps()}
												>
													{cell.render('Cell')}
												</td>)
										})}
									</motion.tr>
								);
							})}
						</tbody>

					</table>
				</div>
				<div className="pagination-container">
					<button
						className="pagination-button"
						onClick={() => gotoPage(0)}
						disabled={!canPreviousPage}
					>
						{"<<"}
					</button>
					<button
						className="pagination-button"
						onClick={() => previousPage()}
						disabled={!canPreviousPage}
					>
						{"<"}
					</button>
					<button
						className="pagination-button"
						onClick={() => nextPage()}
						disabled={!canNextPage}
					>
						{">"}
					</button>
					<button
						className="pagination-button"
						onClick={() => gotoPage(pageCount - 1)}
						disabled={!canNextPage}
					>
						{">>"}
					</button>
					<span className="pagination-info">
						Page{" "}
						<strong>
							{pageIndex + 1} of {pageOptions.length}
						</strong>
					</span>
					<span className="pagination-goto">
						| Go to page:{" "}
						<input
							type="number"
							defaultValue={pageIndex + 1}
							onChange={(e) => {
								const page = e.target.value ? Number(e.target.value) - 1 : 0;
								gotoPage(page);
							}}
							className="pagination-input"
						/>
					</span>
					<select
						className="pagination-select"
						value={pageSize}
						onChange={(e) => {
							setPageSize(Number(e.target.value));
						}}
					>
						{[10, 20, 30, 40, 50].map((pageSize) => (
							<option key={pageSize} value={pageSize}>
								Show {pageSize}
							</option>
						))}
					</select>
				</div>

			</motion.div> : ""
	);
};
export default RatingsTable;
