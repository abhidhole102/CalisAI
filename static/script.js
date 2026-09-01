const form = document.getElementById("form");
const result = document.getElementById("result");


function validateInputs(
    pullUps,
    dips,
    pushUps,
    goal,
    trainingDays
) {

    if (
        pullUps < 0 ||
        dips < 0 ||
        pushUps < 0
    ) {
        return false;
    }

    if (goal === "") {
        return false;
    }

    if (trainingDays === "") {
        return false;
    }

    return true;
}


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    // Prevent multiple requests
    const generateButton = form.querySelector(".generate");

    if (generateButton.disabled) {
        return;
    }

    generateButton.disabled = true;
    generateButton.textContent = "BUILDING YOUR PLAN...";

    result.classList.remove("hidden");

    result.innerHTML = `
    <div class="ai-loading">
        <div class="loading-mark">CALISAI</div>
        <h3>BUILDING YOUR PLAN...</h3>
        <p>
            Analyzing your strength, goal, equipment
            and current skill.
        </p>
        <div class="loading-line"></div>
    </div>
`;

    generateButton.disabled = false;
    generateButton.textContent = "GENERATE MY PLAN ↗";


    const pullUps =
        Number(document.getElementById("pullups").value);

    const dips =
        Number(document.getElementById("dips").value);

    const pushUps =
        Number(document.getElementById("pushups").value);

    const goal =
        document.getElementById("goal").value;

    const trainingDays =
        document.getElementById("days").value;

    const equipment =
        document.getElementById("equipment").value;

    const currentSkill =
        document.getElementById("currentSkill").value;


    const isValid = validateInputs(
        pullUps,
        dips,
        pushUps,
        goal,
        trainingDays
    );


    if (!isValid) {

        result.classList.remove("hidden");

        result.innerHTML = `
            <h3>CHECK YOUR INPUTS</h3>

            <p>
                Please enter valid information
                before generating your plan.
            </p>
        `;

        return;
    }


    try {

        let response;
        let data;

        try {

            response = await fetch("/api/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    pullUps: pullUps,
                    dips: dips,
                    pushUps: pushUps,
                    goal: goal,
                    trainingDays: trainingDays,
                    equipment: equipment,
                    currentSkill: currentSkill
                })
            });

            data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Request failed");
            }

        } catch (error) {

            console.error("CalisAI Error:", error);

            result.classList.remove("hidden");

            result.innerHTML = `
        <div class="ai-error">
            <div class="error-mark">CALISAI</div>

            <h3>AI TEMPORARILY UNAVAILABLE</h3>

            <p>
                We couldn't generate your workout right now.
                This may be because the AI service is temporarily
                busy or your request limit has been reached.
            </p>

            <p class="sub">
                Please wait a little and try again.
            </p>
        </div>
    `;

            generateButton.disabled = false;
            generateButton.textContent = "GENERATE MY PLAN ↗";

            return;
        }

        const level = data.level;
        const aiWorkout = data.aiWorkout;


        result.classList.remove("hidden");


        result.innerHTML = `

            <h3>
                CALISAI AI PLAN / ${level.toUpperCase()}
            </h3>

            <p>
                <b>Goal:</b> ${data.goal}
                &nbsp; • &nbsp;
                <b>Training:</b> ${data.trainingDays} days/week
            </p>

            <p class="sub">
                ${aiWorkout.summary}
            </p>


            <h4>AI Personalized Workout</h4>


            ${aiWorkout.days.map(function (day) {

            return `

                    <div class="workout-day">

                        <h4>
                            DAY ${day.day} — ${day.focus}
                        </h4>

                        <ul>

                            ${day.exercises.map(function (exercise) {

                return `

                                    <li>

                                        <b>${exercise.name}</b>

                                        <br>

                                        Sets: ${exercise.sets}
                                        &nbsp; | &nbsp;

                                        Reps: ${exercise.reps}
                                        &nbsp; | &nbsp;

                                        Rest: ${exercise.rest}

                                    </li>

                                `;

            }).join("")}

                        </ul>

                    </div>

                `;

        }).join("")}


            <h4>Progression</h4>

            <ol>

                ${aiWorkout.progression.map(function (step) {

            return `<li>${step}</li>`;

        }).join("")}

            </ol>


            <h4>Technique Tips</h4>

            <ul>

                ${aiWorkout.tips.map(function (tip) {

            return `<li>${tip}</li>`;

        }).join("")}

            </ul>


            <p class="sub">

                Plan generated by CalisAI AI based on your
                current ability, goal, equipment and skill.

            </p>
        `;

    }

    catch (error) {

        console.error(error);

        result.classList.remove("hidden");

        result.innerHTML = `

            <h3>AI PLAN ERROR</h3>

            <p>
                Something went wrong while generating
                your personalized workout.
            </p>

            <p class="sub">
                Please try again.
            </p>

        `;

    }

});

// Skill card -> AI Coach
document.querySelectorAll(".skill-start").forEach(button => {

    button.addEventListener("click", function () {

        const selectedGoal = this.dataset.goal;

        const goalSelect = document.getElementById("goal");

        if (goalSelect) {
            goalSelect.value = selectedGoal;
        }

    });

});