import { h } from "preact";
import { useState, useEffect } from "preact/hooks";

const Table = () => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(undefined);
  const [sortKey, setSortKey] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  useEffect(() => {
    fetch("/data.json")
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((error) => setError(error));
  }, []);

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortOrder("asc");
    }
  };

  const sortedData = [...data].sort((a, b) => {
    if (!sortKey) {
      return 0;
    }

    const aValue = a[sortKey];
    const bValue = b[sortKey];

    return sortOrder === "asc"
      ? aValue.localeCompare(bValue)
      : bValue.localeCompare(aValue);
  });

  return (
    <>
      {error && (
        <span className="badge badge-error m-2">
          Error al cargar la informacion
        </span>
      )}
      <table className="table">
        <thead>
          <tr>
            <th onClick={() => handleSort("autor")} className="cursor-pointer">
              Autor{" "}
              {sortKey === "autor" && (
                <span>{sortOrder === "asc" ? " ▲" : " ▼"}</span>
              )}
            </th>
            <th>Cita</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((item, index) => (
            <tr key={index}>
              <td>{item["autor"]}</td>
              <td>{item["cita"]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
};

export default Table;
