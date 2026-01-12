export default function ClaimStatus() {
  // allowed values: submitted | in-progress | completed | rejected
  const currentStatus = "in-progress";

  const steps = [
    { key: "submitted", label: "Submitted" },
    { key: "in-progress", label: "In Progress" },
    { key: "completed", label: "Completed" },
    { key: "rejected", label: "Rejected" },
  ];

  const getStepClass = (stepKey: string) => {
    const currentIndex = steps.findIndex(
      (step) => step.key === currentStatus
    );
    const stepIndex = steps.findIndex(
      (step) => step.key === stepKey
    );

    if (stepIndex < currentIndex) return "step completed";
    if (stepIndex === currentIndex) return "step active";
    return "step";
  };

  return (
    <div className="card">
      <h3>Claim Status</h3>

      <p className="success">👍 Claim Successfully Submitted!</p>
      <p>
        Your claim ID is <strong>CL-10231</strong>
      </p>

      {/* Progress Bar */}
      <div className="progress-container">
        {steps.map((step) => (
          <div
            key={step.key}
            className={getStepClass(step.key)}
          >
            <div className="circle"></div>
            <span>{step.label}</span>
          </div>
        ))}
      </div>

      {/* Claim Info */}
      <div className="details">
        <p><strong>Insurance:</strong> Health</p>
        <p><strong>Claim Amount:</strong> $5,000</p>
        <p><strong>Location:</strong> New York</p>
      </div>
    </div>
  );
}
