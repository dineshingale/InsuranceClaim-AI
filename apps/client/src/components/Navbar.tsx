export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">InsuranceClaimFusion AI</div>
      <div className="nav-links">
        <a href="/">Submit Claim</a>
        <a href="/admin" style={{ marginLeft: '1rem' }}>Admin</a>
      </div>
    </nav>
  )
}
