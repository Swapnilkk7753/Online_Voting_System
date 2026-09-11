// Example result data (replace with API / backend later)
const results = [
    { name: "Candidate A", votes: 120 },
    { name: "Candidate B", votes: 95 },
    { name: "Candidate C", votes: 60 }
  ];
  
  // Sort by votes
  results.sort((a, b) => b.votes - a.votes);
  
  // Calculations
  const totalVotes = results.reduce((sum, c) => sum + c.votes, 0);
  const winner = results[0];
  
  // Update summary
  document.getElementById("totalCandidates").innerText = results.length;
  document.getElementById("totalVotes").innerText = totalVotes;
  document.getElementById("winnerName").innerText = winner.name;
  
  // Render results
  const resultBox = document.getElementById("resultBox");
  
  results.forEach((candidate, index) => {
    const percent = ((candidate.votes / totalVotes) * 100).toFixed(1);
  
    resultBox.innerHTML += `
      <div class="col-md-4">
        <div class="glass-card ${index === 0 ? 'winner' : ''}">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h5>
              ${index === 0 ? '🏆 ' : ''}${candidate.name}
            </h5>
            <span class="badge bg-primary rank-badge">
              Rank #${index + 1}
            </span>
          </div>
  
          <p>Votes: <strong>${candidate.votes}</strong></p>
  
          <div class="progress mb-2">
            <div class="progress-bar bg-success"
                 style="width:${percent}%">
            </div>
          </div>
  
          <small>${percent}% of total votes</small>
        </div>
      </div>
    `;
  });
  