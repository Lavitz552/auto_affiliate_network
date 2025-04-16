import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Analytics() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/dashboard')
      .then(res => setData(res.data))
      .catch(() => setData({ message: 'Unable to load analytics. Is the backend running?' }));
  }, []);

  return (
    <div style={{ padding: 32, fontFamily: 'sans-serif' }}>
      <h1>Analytics Dashboard</h1>
      {data ? (
        <pre style={{ background: '#f5f5f5', padding: 16 }}>{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
