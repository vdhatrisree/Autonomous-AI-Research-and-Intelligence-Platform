import ReactMarkdown from "react-markdown";

function ReportView({ result }) {
  if (!result) return null;

  return (
    <div className="dossier">
      <div className="eyebrow">Case File No. {result.session_id}</div>
      <h2>{result.question}</h2>
      <div className="report-text">
        <ReactMarkdown>{result.report}</ReactMarkdown>
      </div>

      <div className="claims-heading">Verified Claims</div>
      {result.verified_claims.map((claim, i) => (
        <div key={i} className="claim">
          <span className={`stamp ${claim.confidence.toLowerCase()}`}>
            {claim.confidence} confidence
          </span>
          <p className="claim-text">{claim.claim}</p>
          <div className="claim-source">Source: {claim.source} · score {claim.score}</div>
        </div>
      ))}
    </div>
  );
}

export default ReportView;