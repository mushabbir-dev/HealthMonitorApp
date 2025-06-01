import DecryptViewer from './components/DecryptViewer';
import LiveDashboard from './components/LiveDashboard';

function App() {
  return (
    <div style={{ maxWidth: 1000, margin: 'auto', padding: '2rem' }}>
      <h1>🩺 Health Monitor Viewer</h1>
      <DecryptViewer />
      <LiveDashboard />
    </div>
  );
}

export default App;
