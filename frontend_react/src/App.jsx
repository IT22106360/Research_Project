import { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const [photoTaken, setPhotoTaken] = useState(false);
  const [imageURL, setImageURL] = useState(null);

  // Start camera on load
  useEffect(() => {
    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: { exact: "environment" } }, // rear camera
          audio: false,
        });

        videoRef.current.srcObject = stream;
      } catch (err) {
        console.error("Camera access error:", err);
      }
    }

    startCamera();
  }, []);

  // Capture photo
  const takePhoto = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    const dataUrl = canvas.toDataURL("image/png");
    setImageURL(dataUrl);
    setPhotoTaken(true);
  };

  // Retake photo
  const retakePhoto = () => {
    setPhotoTaken(false);
    setImageURL(null);
  };

  return (
    <div className="app-container">
      <h1>Mobile Camera Capture</h1>

      {!photoTaken ? (
        <>
          <video ref={videoRef} autoPlay playsInline className="camera-view" />
          <button onClick={takePhoto} className="capture-btn">
            Capture Photo
          </button>
        </>
      ) : (
        <>
          <img src={imageURL} alt="Captured" className="preview-image" />
          <button onClick={retakePhoto} className="capture-btn">
            Retake
          </button>
        </>
      )}

      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
}

export default App;
