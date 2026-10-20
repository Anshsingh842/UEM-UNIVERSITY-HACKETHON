"use strict";

// Koi bhi detail browser mein save nahi hoti (no localStorage / cookies).

const T = {
  hi: {
    title: "जन सहायक",
    subtitle: "जानिए आपको कौन सी सरकारी योजना मिल सकती है",
    langBtn: "English",
    formTitle: "अपनी जानकारी भरें",
    age: "उम्र (साल)",
    state: "राज्य",
    occupation: "काम",
    income: "सालाना आमदनी (₹)",
    gender: "लिंग",
    choose: "चुनें",
    occ_farmer: "किसान",
    occ_student: "विद्यार्थी",
    occ_worker: "असंगठित मज़दूर",
    occ_business: "छोटा व्यापार",
    occ_shop: "दुकानदार",
    occ_self: "स्वरोज़गार",
    occ_other: "कुछ और",
    male: "पुरुष",
    female: "महिला",
    genderOther: "अन्य",
    submit: "योजनाएँ खोजें",
    loading: "खोज रहे हैं...",
    matchTitle: "आपको ये योजनाएँ मिल सकती हैं",
    unsureTitle: "पक्का नहीं — आधिकारिक साइट पर जाँच करें",
    benefit: "कितना फ़ायदा",
    documents: "कौन से कागज़ चाहिए",
    link: "आधिकारिक वेबसाइट खोलें",
    why: "वजह",
    noMatch: "अभी कोई पक्की योजना नहीं मिली।",
    note: "योजनाओं की जानकारी हिंग्लिश में है। नियम राज्य के हिसाब से अलग हो सकते हैं, आवेदन से पहले आधिकारिक साइट देखें।",
    draftBtn: "RTI ड्राफ़्ट बनाएँ",
    draftTitle: "RTI या शिकायत पत्र बनाएँ",
    dtype: "पत्र का प्रकार",
    rti: "RTI (सूचना का अधिकार)",
    complaint: "शिकायत पत्र",
    name: "आपका नाम",
    address: "आपका पता",
    office: "कार्यालय / विभाग का नाम",
    subject: "विषय",
    details: "ब्यौरा (क्या जानकारी चाहिए या क्या शिकायत है)",
    makeDraft: "ड्राफ़्ट बनाएँ",
    letter: "आपका पत्र",
    copy: "कॉपी करें",
    copied: "कॉपी हो गया ✓",
    privacy: "आपकी जानकारी कहीं सेव नहीं की जाती।",
    errNetwork: "सर्वर से जुड़ नहीं पाए। चेक करें कि app चल रहा है।",
    errGeneric: "कुछ गड़बड़ हुई। दोबारा कोशिश करें।",
    errAge: "उम्र 0 से 120 के बीच भरें।",
    errIncome: "सालाना आमदनी का नंबर भरें।",
    errFill: "सभी खाने भरें।",
  },
  en: {
    title: "Jan Sahayak",
    subtitle: "Find out which government schemes you may get",
    langBtn: "हिन्दी",
    formTitle: "Fill your details",
    age: "Age (years)",
    state: "State",
    occupation: "Occupation",
    income: "Yearly income (₹)",
    gender: "Gender",
    choose: "Choose",
    occ_farmer: "Farmer",
    occ_student: "Student",
    occ_worker: "Unorganised worker",
    occ_business: "Small business",
    occ_shop: "Shopkeeper",
    occ_self: "Self employed",
    occ_other: "Something else",
    male: "Male",
    female: "Female",
    genderOther: "Other",
    submit: "Find schemes",
    loading: "Searching...",
    matchTitle: "Schemes you may get",
    unsureTitle: "Not sure — please check the official site",
    benefit: "Benefit",
    documents: "Documents needed",
    link: "Open official website",
    why: "Reason",
    noMatch: "No confirmed scheme found right now.",
    note: "Scheme details are written in Hinglish. Rules can differ by state, so check the official site before applying.",
    draftBtn: "Make RTI draft",
    draftTitle: "Make an RTI or complaint letter",
    dtype: "Letter type",
    rti: "RTI (Right to Information)",
    complaint: "Complaint letter",
    name: "Your name",
    address: "Your address",
    office: "Office / department name",
    subject: "Subject",
    details: "Details (what you want to know or complain about)",
    makeDraft: "Make draft",
    letter: "Your letter",
    copy: "Copy",
    copied: "Copied ✓",
    privacy: "Your details are not saved anywhere.",
    errNetwork: "Could not reach the server. Check that the app is running.",
    errGeneric: "Something went wrong. Please try again.",
    errAge: "Enter an age between 0 and 120.",
    errIncome: "Enter your yearly income as a number.",
    errFill: "Please fill all fields.",
  },
};

let lang = "hi";
let lastResult = null; // sirf screen ke liye, memory mein

const $ = (id) => document.getElementById(id);
const t = (key) => T[lang][key];

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text; // textContent: safe, HTML nahi chalta
  return node;
}

function applyLang() {
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const value = T[lang][node.dataset.i18n];
    if (value !== undefined) node.textContent = value;
  });
  $("langBtn").textContent = t("langBtn");
  document.querySelector(".note").textContent = t("privacy");
  if (lastResult) renderResults(lastResult);
}

function showError(id, message) {
  const box = $(id);
  box.textContent = message;
  box.hidden = false;
}

function hideError(id) {
  $(id).hidden = true;
}

function safeHttps(url) {
  return typeof url === "string" && url.startsWith("https://") ? url : null;
}

function buildCard(item, unsure) {
  const card = el("article", unsure ? "card unsure" : "card");
  card.appendChild(el("h3", "", item.name));

  card.appendChild(el("p", "label", t("benefit")));
  card.appendChild(el("p", "", item.benefit_amount));

  card.appendChild(el("p", "label", t("documents")));
  const list = el("ul");
  (item.documents || []).forEach((doc) => list.appendChild(el("li", "", doc)));
  card.appendChild(list);

  if (unsure && item.reason) {
    card.appendChild(el("p", "why", t("why") + ": " + item.reason));
  }

  const url = safeHttps(item.official_url);
  if (url) {
    const a = el("a", "link", t("link"));
    a.href = url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    card.appendChild(a);
  }
  return card;
}

function renderResults(data) {
  const box = $("results");
  box.replaceChildren();

  const matching = data.matching || [];
  const unsure = data.pakka_nahi_verify_karo || [];

  if (matching.length === 0 && unsure.length === 0) {
    box.appendChild(el("p", "empty", t("noMatch")));
    return;
  }

  if (matching.length) {
    box.appendChild(el("h2", "section-title", t("matchTitle")));
    matching.forEach((item) => box.appendChild(buildCard(item, false)));
  } else {
    box.appendChild(el("p", "empty", t("noMatch")));
  }

  if (unsure.length) {
    box.appendChild(el("h2", "section-title warn", t("unsureTitle")));
    unsure.forEach((item) => box.appendChild(buildCard(item, true)));
  }

  box.appendChild(el("p", "note", t("note")));
}

async function postJSON(path, payload) {
  let response;
  try {
    response = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    return { ok: false, message: t("errNetwork") };
  }
  let data = null;
  try {
    data = await response.json();
  } catch (e) {
    return { ok: false, message: t("errGeneric") };
  }
  if (!response.ok) return { ok: false, message: data && data.error ? data.error : t("errGeneric") };
  return { ok: true, data };
}

// ---------------------------------------------------------- /check form
$("checkForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError("checkError");

  const age = parseInt($("age").value, 10);
  const income = parseFloat($("income").value);
  const state = $("state").value.trim();
  const occupation = $("occupation").value;
  const gender = $("gender").value;

  if (Number.isNaN(age) || age < 0 || age > 120) return showError("checkError", t("errAge"));
  if (Number.isNaN(income) || income < 0) return showError("checkError", t("errIncome"));
  if (!state || !occupation || !gender) return showError("checkError", t("errFill"));

  const button = $("checkBtn");
  button.disabled = true;
  button.textContent = t("loading");

  const result = await postJSON("/check", { age, state, occupation, income, gender });

  button.disabled = false;
  button.textContent = t("submit");

  if (!result.ok) return showError("checkError", result.message);
  lastResult = result.data;
  renderResults(lastResult);
  $("results").scrollIntoView({ behavior: "smooth", block: "start" });
});

// ---------------------------------------------------------- /draft form
$("draftToggle").addEventListener("click", () => {
  const form = $("draftForm");
  form.hidden = !form.hidden;
  if (!form.hidden && !$("dstate").value) $("dstate").value = $("state").value;
  if (!form.hidden) $("dname").focus();
});

$("draftForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError("draftError");

  const payload = {
    type: $("dtype").value,
    language: lang === "hi" ? "hi" : "en",
    name: $("dname").value.trim(),
    address: $("daddress").value.trim(),
    state: $("dstate").value.trim(),
    office: $("doffice").value.trim(),
    subject: $("dsubject").value.trim(),
    details: $("ddetails").value.trim(),
  };
  if (Object.values(payload).some((v) => !v)) return showError("draftError", t("errFill"));

  const button = $("draftBtn");
  button.disabled = true;
  button.textContent = t("loading");

  const result = await postJSON("/draft", payload);

  button.disabled = false;
  button.textContent = t("makeDraft");

  if (!result.ok) return showError("draftError", result.message);
  $("letter").value = result.data.letter;
  $("letterBox").hidden = false;
  $("letterBox").scrollIntoView({ behavior: "smooth", block: "start" });
});

$("copyBtn").addEventListener("click", async () => {
  const text = $("letter").value;
  try {
    await navigator.clipboard.writeText(text);
  } catch (e) {
    $("letter").select();
    document.execCommand("copy");
  }
  $("copyBtn").textContent = t("copied");
  setTimeout(() => ($("copyBtn").textContent = t("copy")), 2000);
});

// ---------------------------------------------------------- language
$("langBtn").addEventListener("click", () => {
  lang = lang === "hi" ? "en" : "hi";
  applyLang();
});

applyLang();
