// ===== Sample votes data =====
const votes = {
    "Rohit": 75,
    "Anita": 55,
    "Suresh": 90,
    "Neha": 40
  };
  
  // Calculate total votes
  const totalVotes = Object.values(votes).reduce((a,b)=>a+b,0);
  
  // Animate progress bars
  function updateResults() {
    Object.keys(votes).forEach(name => {
      const progressBar = document.getElementById(`progress-${name}`);
      if(progressBar){
        const percentage = (votes[name]/totalVotes)*100;
        progressBar.style.width = `${percentage}%`;
        progressBar.textContent = `${votes[name]} Votes`;
      }
    });
  }
  
  // Call on page load
  window.addEventListener('DOMContentLoaded', updateResults);
  