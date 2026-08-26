import { useState, useEffect } from "react";
import { doResearch, listSessions } from "./api/client";
import ResearchForm from "./components/ResearchForm";
import ReportView from "./components/ReportView";
import SessionList from "./components/SessionList";
import ChatBox from "./components/ChatBox";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [activeChatSession, setActiveChatSession] = useState(null);

  const refreshSessions = async () => {
    const data = await listSessions();
    setSessions(data);
  };

  useEffect(() => {
    refreshSessions();
  }, []);

  const handleResearch = async (question) => {
    setLoading(true);
    const data = await doResearch(question);
    setResult(data);
    setActiveChatSession(data.session_id);
    setLoading(false);
    refreshSessions();
  };

  return (
    <div className="app">
      <header className="catalog-header">
        <div className="eyebrow">Research Archive · Evidence-Verified</div>
        <h1>Autonomous Research Desk</h1>
      </header>

      <ResearchForm onSubmit={handleResearch} loading={loading} />

      <div className="main-layout">
        <div className="left-panel">
          {result ? (
            <ReportView result={result} />
          ) : (
            <p className="empty-note">No case file open. Submit a question above to begin.</p>
          )}
        </div>
        <div className="right-panel">
          <SessionList sessions={sessions} onSelect={setActiveChatSession} />
          {activeChatSession && <ChatBox sessionId={activeChatSession} />}
        </div>
      </div>
    </div>
  );
}

export default App;