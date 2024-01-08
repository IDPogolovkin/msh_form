const prevBtns = document.querySelectorAll(".btn-prev");
const nextBtns = document.querySelectorAll(".btn-next");
const progress = document.getElementById("progress");
const formSteps = document.querySelectorAll(".form-step");
const progressSteps = document.querySelectorAll(".progress-step");
const saveBtn = document.querySelectorAll(".btn");
const errorDiv = document.querySelector(".flash-error");
const otherDiv1 = document.querySelector(".flash-success");
const otherDiv2 = document.querySelector(".flash-info");

let formStepsNum = 0;

saveBtn.forEach((btn) => {
  btn.addEventListener("click", () => {
    const allInputs = Array.from(formSteps).flatMap((formStep) =>
      Array.from(formStep.querySelectorAll("input, select, textarea"))
    );

    // Check if any required input is missing
    let inputsFilled = true;

    allInputs.forEach((input) => {
      input.classList.remove("input-empty");
      if (input.hasAttribute("required") && input.value.trim() === "") {
        inputsFilled = false;
        input.classList.add("input-empty");
      }
    });
    if (otherDiv1){
      otherDiv1.style.display = inputsFilled ? "block" : "none";
    }
    if (otherDiv2){
      otherDiv2.style.display = inputsFilled ? "block" : "none";
    } 
    errorDiv.style.display = inputsFilled ? "none" : "block";
    if (!inputsFilled) {
      // Scroll to the error div if there are missing inputs
      errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  })
})

nextBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    // Check if the current form step has all required inputs filled
    const currentFormStep = formSteps[formStepsNum];
    const requiredInputs = currentFormStep.querySelectorAll('[required]');
    let inputsFilled = true;
    requiredInputs.forEach((input) => {
      input.classList.remove("input-empty");
    });
    requiredInputs.forEach((input) => {
      if (input.value.trim() === '') {
        inputsFilled = false;
        input.classList.add("input-empty");
      }
    });
    errorDiv.style.display = inputsFilled ? "none" : "block";
    if (inputsFilled) {
      formStepsNum++;
      updateFormSteps();
      updateProgressbar();
    }
    else{
      errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});

prevBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    formStepsNum--;
    updateFormSteps();
    updateProgressbar();
  });
});

progressSteps.forEach((progressStep, idx) => {
  progressStep.addEventListener("click", () => {
    formStepsNum = Array.from(progressSteps).indexOf(progressStep);
    updateFormSteps();
    updateProgressbar();
  });
});

function updateFormSteps() {
  formSteps.forEach((formStep) => {
    formStep.classList.contains("form-step-active") &&
      formStep.classList.remove("form-step-active");
  });

  formSteps[formStepsNum].classList.add("form-step-active");
}

function updateProgressbar() {
progressSteps.forEach((progressStep, idx) => {
  if (idx < formStepsNum + 1) {
    progressStep.classList.add("progress-step-active");
  } else {
    progressStep.classList.remove("progress-step-active");
  }
});

const progressActive = document.querySelectorAll(".progress-step-active");

progress.style.width =
((progressActive.length - 1) / (progressSteps.length - 1)) * 100 + "%";
}
