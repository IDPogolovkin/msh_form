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

nextBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
      formStepsNum++;
      updateFormSteps();
      updateProgressbar();
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
