import { useState } from 'react';

export default function DecryptViewer() {
  const [encrypted, setEncrypted] = useState('');
  const [password, setPassword] = useState('');
  const [decrypted, setDecrypted] = useState('');
  const [timeTaken, setTimeTaken] = useState(null);
  const [error, setError] = useState('');

  const handleDecrypt = async () => {
    setError('');
    setDecrypted('');
    setTimeTaken(null);

    try {
      const res = await fetch('http://127.0.0.1:5000/api/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ encrypted, password })
      });
      const data = await res.json();

      if (data.status === 'success') {
        setDecrypted(JSON.stringify(data.decrypted, null, 2));
        setTimeTaken(data.decryption_time);
      } else {
        setError(data.message || 'Decryption failed.');
      }
    } catch (err) {
      setError('Connection failed.');
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '1rem', marginBottom: '2rem' }}>
      <h2>🔓 Decrypt Viewer</h2>
      <textarea
        placeholder="Paste encrypted data..."
        rows={5}
        style={{ width: '100%' }}
        value={encrypted}
        onChange={(e) => setEncrypted(e.target.value)}
      />
      <input
        type="password"
        placeholder="Enter password"
        style={{ marginTop: '0.5rem', width: '100%' }}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleDecrypt} style={{ marginTop: '1rem' }}>
        Decrypt
      </button>
      {decrypted && (
        <pre style={{ background: '#f4f4f4', marginTop: '1rem' }}>
          {decrypted}
          {timeTaken && `\n\n🕒 Decryption Time: ${timeTaken} sec`}
        </pre>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}
