import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FilterData.css';
import styles from './FilterData.css';
import Pagination from 'react-paginate';

const FilterData = () => {
  const [columns, setColumns] = useState([]);
  const [selectedColumn, setSelectedColumn] = useState('');
  const [selectedData, setSelectedData] = useState('');
  const [columnData, setColumnData] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);

  useEffect(() => {
    const cachedColumns = localStorage.getItem('columns');
    if (cachedColumns) {
      setColumns(JSON.parse(cachedColumns));
    } else {
      const fetchColumns = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/');
        setColumns(response.data.columns);
        localStorage.setItem('columns', JSON.stringify(response.data.columns));
      } catch (error) {
        console.error(error);
      }
    };

    fetchColumns();
    }
  }, []);

useEffect(() => {
    if (!selectedColumn) return;
  const fetchData = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/fetch_data', {
          column: selectedColumn,
      });
      setColumnData(response.data.rows);
    } catch (error) {
      console.error(error);
    }
  };
  fetchData();
}, [selectedColumn]);

useEffect(() => {
    if (!selectedData) return;
    const fetchRows = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/fetch_rows', {
          column: selectedColumn,
          data: selectedData,
          page: currentPage,
          limit: itemsPerPage,
      });
        setTableData(response.data.rows);
        console.log(tableData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchRows();
  }, [selectedColumn, selectedData, currentPage, itemsPerPage]);

    const handleColumnChange = (e) => {
        setSelectedColumn(e.target.value);
        setColumnData([]);
        setTableData([]);
    };

    const handleDataChange = (e) => {
        setSelectedData(e.target.value);
    };

    const handlePageChange = (data) => {
    setCurrentPage(data.selected + 1);
  };

  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const slicedData = tableData.slice(startIndex, endIndex);

  return (
    <div>
      <div className="floating-filters">
        <label><b>Select a Column</b></label>
        <div>
        <select value={selectedColumn} onChange={handleColumnChange}>
        <option value="">Select a Column</option>
        {columns.map((column) => (
          <option key={column} value={column}>
            {column}
          </option>
        ))}
      </select>
        </div>
        {columnData.length > 0 && (<label><b>Select a Value</b></label>)}
        <div>
        {columnData.length > 0 && (
        <select value={selectedData} onChange={handleDataChange}>
        <option value="">Select a Type</option>
        {columnData.map((data) => (
          <option key={data} value={data}>
            {data}
          </option>
        ))}
      </select>
      )}
        </div>
      </div>
      {slicedData.length > 0 && (
        <table className="excel-table">
          <thead>
            <tr>
              {columns &&
                columns.map((header) => (
                  <th>{header}</th>
                ))}
            </tr>
          </thead>
          <tbody>
            {slicedData.map((row) => (
              <tr key={row.id || Math.random()}>
                {Object.values(row).map((cell) => (
                  <td key={cell}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <Pagination
        initialPage={currentPage - 1}
        pageCount={Math.ceil(tableData.length / itemsPerPage)}
        onPageChange={handlePageChange}
        pageSize={itemsPerPage}
      />
    </div>
  );
};

export default FilterData;