import { motion } from "framer-motion";
import { Edit, Search, Trash2 } from "lucide-react";
import { useState, useMemo } from "react";
import { useTable, usePagination } from "react-table";
const RATING_DATA = [
	{ id: 1, name: "Wireless Earbuds", category: "Electronics", price: 59.99, stock: 143, sales: 1200 },
];
const RATING_COLUMNS = [
	{
		Header: "First Name",
		accessor: "id"
	},
	{
		Header: "First Name",
		accessor: "name"
	},
	{
		Header: "First Name",
		accessor: "category"
	},
	{
		Header: "First Name",
		accessor: "price"
	},
	{
		Header: "First Name",
		accessor: "stock"
	},
	{
		Header: "First Name",
		accessor: "sales"
	},
];
const INITIAL_STATE = {
	pageSize: 10,
	pageIndex: 0
};
const RatingsTable = ({ ratingdata }) => {

	const data = useMemo(() => RATING_DATA, [RATING_DATA]);
	const columns = useMemo(() => RATING_COLUMNS, [RATING_COLUMNS]);
	const initialState = useMemo(() => INITIAL_STATE, [INITIAL_STATE]);

	const [searchTerm, setSearchTerm] = useState("");
	const [filteredRatings, setFilteredRatings] = useState(ratingdata.slice(0, 50));

	const handleSearch = (e) => {
		const term = e.target.value.toLowerCase();
		setSearchTerm(term);
		const filtered = ratingdata.filter(
			(rating) => rating.name.toLowerCase().includes(term) || rating.category.toLowerCase().includes(term)
		);

		setFilteredRatings(filtered);
	};

	// Use the state and functions returned from useTable to build your UI
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
			columns,
			data,
			initialState
		},
		usePagination // highlight-line
	);

	return (
		<>
			<table {...getTableProps()}>
				<thead>
					{headerGroups.map((headerGroup) => (
						<tr {...headerGroup.getHeaderGroupProps()}>
							{headerGroup.headers.map((column) => (
								<th {...column.getHeaderProps()}>{column.render("Header")}</th>
							))}
						</tr>
					))}
				</thead>
				<tbody {...getTableBodyProps()}>
					{page.map((row, i) => { // highlight-line
						prepareRow(row);
						return (<motion.tr
							key={row.id}
							initial={{ opacity: 0 }}
							animate={{ opacity: 1 }}
							transition={{ duration: 0.3 }}
						>
							{row.cells.map((cell) => {
								return (
									<td className='px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-100 flex gap-2 items-center' {...cell.getCellProps()}>{"cell.render(Cell)"}</td>
								);
							})}
						</motion.tr>
						);
					})}
				</tbody>
			</table>
			<div className="pagination">
				<button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
					{"<<"}
				</button>{" "}
				<button onClick={() => previousPage()} disabled={!canPreviousPage}>
					{"<"}
				</button>{" "}
				<button onClick={() => nextPage()} disabled={!canNextPage}>
					{">"}
				</button>{" "}
				<button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>
					{">>"}
				</button>{" "}
				<span>
					Page{" "}
					<strong>
						{pageIndex + 1} of {pageOptions.length}
					</strong>{" "}
				</span>
				<span>
					| Go to page:{" "}
					<input
						type="number"
						defaultValue={pageIndex + 1}
						onChange={(e) => {
							const page = e.target.value ? Number(e.target.value) - 1 : 0;
							gotoPage(page);
						}}
						style={{ width: "100px" }}
					/>
				</span>{" "}
				<select
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
		</>
	);
};
export default RatingsTable;
