import { Routes, Route } from "react-router-dom"
import SubmitClaim from "./pages/SubmitClaim"
import ClaimStatusPage from "./pages/ClaimStatusPage"
import Navbar from "./components/Navbar"

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<SubmitClaim />} />
        <Route path="/status" element={<ClaimStatusPage />} />
      </Routes>
    </>
  )
}

export default App
