async function evaluateIdea() {
    const idea = document.getElementById("idea").value.trim();
    if (!idea) {
        alert("Please enter a business idea");
        return;
    }

    const res = await fetch("/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea })
    });

    const data = await res.json();
    if (res.ok) {
        document.getElementById("score").textContent = `Score: ${data.score}/100`;
        document.getElementById("verdict").textContent = data.verdict;

        document.getElementById("pros").innerHTML = data.pros.map(p => `<li>${p}</li>`).join("");
        document.getElementById("cons").innerHTML = data.cons.map(c => `<li>${c}</li>`).join("");
        document.getElementById("risks").innerHTML = data.risks.map(r => `<li>${r}</li>`).join("");
        document.getElementById("next-steps").innerHTML = data.next_steps.map(s => `<li>${s}</li>`).join("");

        document.getElementById("results").classList.remove("hidden");
    } else {
        alert(data.error || "Something went wrong");
    }
}
