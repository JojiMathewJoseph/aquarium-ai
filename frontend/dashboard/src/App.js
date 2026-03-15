import { useEffect, useState } from "react";

export default function App() {

  const [fishCount, setFishCount] = useState(0);
  const [confidence, setConfidence] = useState(0);

  const cameraUrl = "http://192.168.2.60:8080/video";

  const fetchLatest = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/fish/latest");
      const data = await res.json();

      setFishCount(data.fish_count || 0);
      setConfidence(data.confidence || 0);

    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {

    fetchLatest();

    const interval = setInterval(() => {
      fetchLatest();
    }, 5000);

    return () => clearInterval(interval);

  }, []);

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>

      <h1>🐟 Aquarium AI Dashboard</h1>

      <h2>System Status</h2>
      <p>Camera: Connected</p>
      <p>Detection Model: Active</p>

      <h2>Latest Detection</h2>
      <p>Fish Count: {fishCount}</p>
      <p>Confidence: {confidence}</p>

      <h2>Camera Feed</h2>

      <img
        src={cameraUrl}
        alt="Camera Feed"
        style={{ width: "700px", borderRadius: "10px" }}
      />

    </div>
  );
}