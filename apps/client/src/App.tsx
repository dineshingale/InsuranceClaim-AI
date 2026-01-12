import { Routes, Route } from "react-router-dom"
import SubmitClaim from "./pages/SubmitClaim"
import ClaimStatusPage from "./pages/ClaimStatusPage"
import AdminDashboard from "./pages/AdminDashboard"
import Navbar from "./components/Navbar"
import { useEffect, useState } from "react"

function App() {
  const [serverMessage, setServerMessage] = useState<string>("")

  useEffect(() => {
    fetch("http://localhost:8000/")
      .then((res) => res.json())
      .then((data) => setServerMessage(data.message))
      .catch((err) => console.error("Failed to fetch from server:", err))
  }, [])

  return (
    <>
      <Navbar />
      {serverMessage && (
        <div className="notification">
          📡 Server Connected: {serverMessage}
        </div>
      )}
      <Routes>
        <Route path="/" element={<SubmitClaim />} />
        <Route path="/status" element={<ClaimStatusPage />} />
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </>
  )
}

export default App
