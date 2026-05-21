export default function QuickReply({ options, onSelect }) {
  return (
    <div style={{ padding: "12px 16px", display: "flex", flexWrap: "wrap", gap: 8, borderTop: "1px solid #eee" }}>
      {options.map(opt => (
        <button
          key={opt}
          onClick={() => onSelect(opt)}
          style={{
            padding: "8px 16px",
            borderRadius: 20,
            border: "1px solid #ddd",
            background: "#fff",
            cursor: "pointer",
            fontSize: 13,
            transition: "all 0.15s"
          }}
        >
          {opt}
        </button>
      ))}
    </div>
  );
}