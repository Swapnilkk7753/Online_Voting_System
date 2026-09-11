
// ===== VOTING LOGIC =====
  
  function send(id) {
    fetch(`/CanUp/${id}`,{method:"POST"})
  }

  function voterlist(n,e,r,s) {
  fetch(`/Voter_List/${n}/${e}/${r}/${s}`,{method:"POST"})
  }
  
// Load existing votes
