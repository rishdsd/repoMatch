export default function Message({ role, text, loading }) {
  const isBot = role === "bot";
  return (
    <div style={{ display: "flex", justifyContent: isBot ? "flex-start" : "flex-end" }}>
      <div style={{
        maxWidth: "75%",
        padding: "10px 14px",
        borderRadius: isBot ? "4px 16px 16px 16px" : "16px 4px 16px 16px",
        background: isBot ? "#f4f4f4" : "#111",
        color: isBot ? "#111" : "#fff",
        fontSize: 14,
        lineHeight: 1.5
      }}>
        {loading ? <span style={{ opacity: 0.5 }}>thinking...</span> : text}
      </div>
    </div>
  );
}