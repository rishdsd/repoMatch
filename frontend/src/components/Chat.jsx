import { useState, useEffect, useRef } from "react";
import { sendAnswer } from "../api";
import Message from "./Message";
import QuickReply from "./QuickReply";
import RepoCard from "./RepoCard";

const OPENING_STAGE = {
  id: "language",
  question: "Hey! Let's find you an open source repo where you'll actually succeed. What language or stack do you work in most?",
  type: "text",
  hint: "e.g. Python, JavaScript, Go, Rust..."
};

export default function Chat() {
  const [messages, setMessages] = useState([
    { role: "bot", text: OPENING_STAGE.question }
  ]);
  const [currentStage, setCurrentStage] = useState(OPENING_STAGE);
  const [answers, setAnswers] = useState({});
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleAnswer(answer) {
    const stageId = currentStage.id;

    // Show user message
    setMessages(prev => [...prev, { role: "user", text: answer }]);
    setInputText("");
    setLoading(true);

    try {
      const data = await sendAnswer(answers, stageId, answer);

      if (data.status === "complete") {
        console.log("RESULTS:", data.results);  
        setMessages(prev => [...prev, {
          role: "bot",
          text: "Found some great matches for you. Here's where I'd start:"
        }]);
        setResults(data.results);
      } else {
        const next = data.next_stage;
        setCurrentStage(next);
        setAnswers(data.answers);
        setMessages(prev => [...prev, { role: "bot", text: next.question }]);
      }
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "bot",
        text: "Something went wrong. Try again?"
      }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <strong>RepoMatch</strong>
        <span style={styles.subtitle}>Find your first merged PR</span>
      </div>

      <div style={styles.messages}>
        {messages.map((m, i) => (
          <Message key={i} role={m.role} text={m.text} />
        ))}

        {loading && <Message role="bot" text="..." loading />}

        {results && results.map((repo, i) => (
          <RepoCard key={i} repo={repo} />
        ))}

        <div ref={bottomRef} />
      </div>

      {!results && !loading && currentStage && (
        currentStage.type === "quick_reply" ? (
          <QuickReply
            options={currentStage.options}
            onSelect={handleAnswer}
          />
        ) : (
          <div style={styles.inputRow}>
            <input
              style={styles.input}
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              onKeyDown={e => e.key === "Enter" && inputText.trim() && handleAnswer(inputText.trim())}
              placeholder={currentStage.hint || "Type your answer..."}
              autoFocus
            />
            <button
              style={styles.btn}
              onClick={() => inputText.trim() && handleAnswer(inputText.trim())}
            >
              →
            </button>
          </div>
        )
      )}
    </div>
  );
}

const styles = {
  container: { maxWidth: 640, margin: "0 auto", height: "100vh", display: "flex", flexDirection: "column", fontFamily: "system-ui, sans-serif" },
  header: { padding: "16px 20px", borderBottom: "1px solid #eee", display: "flex", alignItems: "baseline", gap: 10 },
  subtitle: { fontSize: 13, color: "#888" },
  messages: { flex: 1, overflowY: "auto", padding: "20px 16px", display: "flex", flexDirection: "column", gap: 12 },
  inputRow: { display: "flex", padding: "12px 16px", gap: 8, borderTop: "1px solid #eee" },
  input: { flex: 1, padding: "10px 14px", borderRadius: 8, border: "1px solid #ddd", fontSize: 14, outline: "none" },
  btn: { padding: "10px 18px", borderRadius: 8, background: "#111", color: "#fff", border: "none", cursor: "pointer", fontSize: 16 }
};