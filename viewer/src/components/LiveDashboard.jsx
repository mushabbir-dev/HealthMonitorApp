import { useEffect, useState } from 'react';
import axios from 'axios';
import './LiveDashboard.css';

function LiveDashboard() {
  const [data, setData] = useState([]);
  const [error, setError] = useState('');
  const [decrypted, setDecrypted] = useState({});

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/encrypted')
      .then(res => setData(res.data.data))
      .catch(() => setError('Connection failed'));
  }, []);

  const handleDecrypt = async (id, encrypted) => {
    const password = prompt('Enter decryption password:');
    if (!password) return;

    try {
      const res = await axios.post('http://127.0.0.1:5000/api/decrypt', {
        encrypted,
        password
      });
      const parsed = JSON.parse(res.data.decrypted.replace(/'/g, '"'));

      setDecrypted(prev => ({
        ...prev,
        [id]: {
          decrypted: parsed,
          time: res.data.decryption_time
        }
      }));
    } catch (err) {
      setDecrypted(prev => ({
        ...prev,
        [id]: { error: '❌ Decryption failed (wrong password or invalid)' }
      }));
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-card">
        <h2 className="dashboard-title">📊 Live Encrypted Data Dashboard</h2>
        {error && <p className="error">{error}</p>}
        {!error && data.length === 0 && <p>No data found.</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Encrypted</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {data.map((entry, idx) => (
                <tr key={entry._id}>
                  <td>{idx + 1}</td>
                  <td title={entry.encrypted_data}>
                    {entry.encrypted_data.slice(0, 30)}...
                  </td>
                  <td>
                    <button onClick={() => handleDecrypt(entry._id, entry.encrypted_data)}>🔓 Decrypt</button>
                    {decrypted[entry._id] && (
                      <div className="decryption-result">
                        {decrypted[entry._id].error ? (
                          <span className="error">{decrypted[entry._id].error}</span>
                        ) : (
                          <ul>
                            <li><strong>📟 Device:</strong> {decrypted[entry._id].decrypted.device_id}</li>
                            <li><strong>💓 Heart Rate:</strong> {decrypted[entry._id].decrypted.heart_rate}</li>
                            <li><strong>🌡 Temperature:</strong> {decrypted[entry._id].decrypted.temperature}°C</li>
                            <li><strong>🕒 Timestamp:</strong> {new Date(decrypted[entry._id].decrypted.timestamp * 1000).toLocaleString()}</li>
                            <li><strong>⏱ Time Taken:</strong> {decrypted[entry._id].time} sec</li>
                          </ul>
                        )}
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default LiveDashboard;
