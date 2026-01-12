import { useNavigate } from "react-router-dom"
import { useState } from "react"

export default function ClaimForm() {
  const navigate = useNavigate()

  // form state
  const [insuranceType, setInsuranceType] = useState("Health")
  const [policyNumber, setPolicyNumber] = useState("")
  const [email, setEmail] = useState("")
  const [dateOfIncident, setDateOfIncident] = useState("")
  const [claimAmount, setClaimAmount] = useState("")
  const [location, setLocation] = useState("")
  const [description, setDescription] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // later this data will go to backend / AI pipeline
    const claimData = {
      insuranceType,
      policyNumber,
      email,
      dateOfIncident,
      claimAmount,
      location,
      description,
    }

    console.log("Submitted Claim:", claimData)

    navigate("/status")
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h3>Claim Submission Form</h3>
      <p className="subtitle">
        This is the data collection layer for your AI pipeline.
      </p>

      <label>Insurance Type *</label>
      <select
        value={insuranceType}
        onChange={(e) => setInsuranceType(e.target.value)}
        required
      >
        <option value="Health">Health</option>
        <option value="Accident">Accident</option>
        <option value="Theft">Theft</option>
      </select>

      <label>Policy Number *</label>
      <input
        type="text"
        value={policyNumber}
        onChange={(e) => setPolicyNumber(e.target.value)}
        required
      />

      <label>Your Email *</label>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />

      {/* DATE + AMOUNT ROW */}
      <div className="row">
        <div>
          <label>Date of Incident *</label>
          <input
            type="date"
            value={dateOfIncident}
            onChange={(e) => setDateOfIncident(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Claim Amount *</label>
          <input
            type="number"
            placeholder="Enter amount"
            value={claimAmount}
            onChange={(e) => setClaimAmount(e.target.value)}
            required
          />
        </div>
      </div>

      <label>Location *</label>
      <input
        type="text"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        required
      />

      <label>Claim Description *</label>
      <textarea
        placeholder="Describe the incident..."
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />

      <label>Upload Documents (optional)</label>
      <input type="file" />

      <button type="submit">Submit Claim</button>
    </form>
  )
}
