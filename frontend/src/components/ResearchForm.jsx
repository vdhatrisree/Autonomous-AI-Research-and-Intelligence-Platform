import { useState } from "react";

function ResearchForm({ onSubmit, loading }) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim()) onSubmit(question);
  };

  return (
    <form className="search-slip" onSubmit={handleSubmit}>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="File a new inquiry..."
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Researching…" : "Open File"}
      </button>
    </form>
  );
}

export default ResearchForm;