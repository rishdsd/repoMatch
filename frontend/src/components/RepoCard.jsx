export default function RepoCard({ repo }) {
  return (
    <div style={{
      border: "1px solid #e5e5e5",
      borderRadius: 12,
      padding: "16px 18px",
      display: "flex",
      flexDirection: "column",
      gap: 10,
      background: "#fff"
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <a href={repo.url} target="_blank" rel="noreferrer"
          style={{ fontWeight: 600, fontSize: 15, color: "#111", textDecoration: "none" }}>
          {repo.name}
        </a>
        <span style={{ fontSize: 12, color: "#888" }}>★ {repo.stars?.toLocaleString()}</span>
      </div>

      <p style={{ fontSize: 13, color: "#555", margin: 0, lineHeight: 1.5 }}>
        {repo.match_reason}
      </p>

      {repo.issue_title && (
        <div style={{ background: "#f8f8f8", borderRadius: 8, padding: "10px 12px" }}>
          <div style={{ fontSize: 11, color: "#888", marginBottom: 4, textTransform: "uppercase", letterSpacing: "0.05em" }}>
            Start here
          </div>
          <a href={repo.issue_url} target="_blank" rel="noreferrer"
            style={{ fontSize: 13, fontWeight: 500, color: "#111", textDecoration: "none" }}>
            {repo.issue_title}
          </a>
          {repo.what_to_do && (
            <p style={{ fontSize: 13, color: "#555", margin: "8px 0 0", lineHeight: 1.5 }}>
              {repo.what_to_do}
            </p>
          )}
          {repo.difficulty && (
            <span style={{
              display: "inline-block",
              marginTop: 8,
              padding: "2px 8px",
              borderRadius: 20,
              fontSize: 11,
              background: repo.difficulty === "easy" ? "#e6f4ea" : repo.difficulty === "moderate" ? "#fef9e7" : "#fdecea",
              color: repo.difficulty === "easy" ? "#2d6a4f" : repo.difficulty === "moderate" ? "#7d6608" : "#922b21"
            }}>
              {repo.difficulty}
            </span>
          )}
        </div>
      )}
    </div>
  );
}