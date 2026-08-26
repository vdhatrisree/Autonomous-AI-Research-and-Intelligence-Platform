function SessionList({ sessions, onSelect }) {
  return (
    <div className="session-list">
      <h3>Filing Cabinet</h3>
      {sessions.length === 0 ? (
        <p className="empty-note">No sessions filed yet.</p>
      ) : (
        sessions.map((s) => (
          <div
            key={s.id}
            className="session-item"
            tabIndex={0}
            onClick={() => onSelect(s.id)}
            onKeyDown={(e) => e.key === "Enter" && onSelect(s.id)}
          >
            <span className="session-id">No. {s.id}</span>
            <span>{s.question}</span>
          </div>
        ))
      )}
    </div>
  );
}

export default SessionList;