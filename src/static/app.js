document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear and populate the select dropdown
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';
      Object.keys(activities).forEach(name => {
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });

      // Render activities with participants
      renderActivities(activities);
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  function renderActivities(activities) {
    activitiesList.innerHTML = "";
    Object.entries(activities).forEach(([name, info]) => {
      const card = document.createElement("div");
      card.className = "activity-card";

      card.innerHTML = `
        <h4>${name}</h4>
        <p>${info.description}</p>
        <p><strong>Schedule:</strong> ${info.schedule}</p>
        <p><strong>Max Participants:</strong> ${info.max_participants}</p>
        <div class="participants-section">
          <h5>Participants:</h5>
          <ul class="participants-list">
            ${info.participants.length > 0
              ? info.participants.map(email => `
                  <li style="display: flex; align-items: center; justify-content: space-between;">
                    <span>${email}</span>
                    <button class="delete-participant" data-activity="${name}" data-email="${email}" title="Remove" style="background: none; border: none; color: #c00; cursor: pointer; font-size: 1.2em; padding: 0;">&#10060;</button>
                  </li>
                `).join("")
              : "<li><em>No participants yet</em></li>"
            }
          </ul>
        </div>
      `;

      activitiesList.appendChild(card);
    });
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        fetchActivities(); // Refresh the activities list to show the new participant
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});

// Add a single event listener for delete buttons (outside DOMContentLoaded to ensure it's attached once)
document.addEventListener("click", async (event) => {
  if (event.target.classList.contains("delete-participant")) {
    event.preventDefault();
    event.stopPropagation();
    
    const activity = event.target.getAttribute("data-activity");
    const email = event.target.getAttribute("data-email");
    
    if (!activity || !email) return;
    
    try {
      const response = await fetch(`/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`, {
        method: "DELETE",
      });
      
      if (response.ok) {
        const messageDiv = document.getElementById("message");
        messageDiv.textContent = `Removed ${email} from ${activity}.`;
        messageDiv.classList.remove("hidden");
        setTimeout(() => {
          messageDiv.classList.add("hidden");
        }, 2000);
        
        // Refresh the activities list
        const activitiesList = document.getElementById("activities-list");
        const activitySelect = document.getElementById("activity");
        const response2 = await fetch("/activities");
        const activities = await response2.json();
        
        // Update select dropdown
        activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';
        Object.keys(activities).forEach(name => {
          const option = document.createElement("option");
          option.value = name;
          option.textContent = name;
          activitySelect.appendChild(option);
        });
        
        // Re-render activities
        activitiesList.innerHTML = "";
        Object.entries(activities).forEach(([name, info]) => {
          const card = document.createElement("div");
          card.className = "activity-card";

          card.innerHTML = `
            <h4>${name}</h4>
            <p>${info.description}</p>
            <p><strong>Schedule:</strong> ${info.schedule}</p>
            <p><strong>Max Participants:</strong> ${info.max_participants}</p>
            <div class="participants-section">
              <h5>Participants:</h5>
              <ul class="participants-list">
                ${info.participants.length > 0
                  ? info.participants.map(email => `
                      <li style="display: flex; align-items: center; justify-content: space-between;">
                        <span>${email}</span>
                        <button class="delete-participant" data-activity="${name}" data-email="${email}" title="Remove" style="background: none; border: none; color: #c00; cursor: pointer; font-size: 1.2em; padding: 0;">&#10060;</button>
                      </li>
                    `).join("")
                  : "<li><em>No participants yet</em></li>"
                }
              </ul>
            </div>
          `;
          activitiesList.appendChild(card);
        });
      } else {
        const errorMsg = await response.text();
        alert("Failed to remove participant: " + errorMsg);
      }
    } catch (error) {
      console.error("Error removing participant:", error);
      alert("Error removing participant.");
    }
  }
});
